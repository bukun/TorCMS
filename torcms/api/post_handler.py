'''
Handler of Posts via Ajax.
'''
import json

import tornado.escape
import tornado.web
from config import post_cfg
from torcms.core import privilege, tools
from torcms.handlers.post_handler import PostHandler
from torcms.model.post_model import MPost
from torcms.model.category_model import MCategory
from torcms.model.user_model import MUser
from torcms.model.staff2role_model import MStaff2Role
from torcms.model.process_model import MState, MTransition, MRequest, MAction, MRequestAction, \
    MTransitionAction, MProcess, MPermissionAction


class ApiPostHandler(PostHandler):
    '''
    Handler of Posts via Ajax.
    '''

    def initialize(self, **kwargs):
        super().initialize()
        self.kind = '9'

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(args[0])

        if url_arr[0] == 'list':
            self.list(url_arr[1])

    def post(self, *args, **kwargs):
        url_str = args[0]

        if url_str == '':
            return
        url_arr = self.parse_url(url_str)

        if url_arr[0] == '_edit':
            self.update(url_arr[1])
        elif url_arr[0] == '_delete':
            self.delete(url_arr[1])
        elif url_arr[0] == 'submit_process':
            self.submit_process()

        elif url_arr[0] == 'amis_submit_action':
            self.amis_submit_action()
        elif url_arr[0] == 'rovoke':
            self.rovoke()


        elif url_arr[0] == 'batch_delete':
            self.batch_delete(url_arr[1])

        else:
            self.redirect('misc/html/404.html')

    def submit_process(self):

        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)[0]

        process_id = post_data['process_id']
        post_id = post_data['post_id']
        user_id = post_data['user_id']
        print("-" * 50)
        act_arr, cur_state_id = self.create_request(process_id, post_id, user_id)
        print(act_arr)
        output = {'act_arr': act_arr}

        return json.dump(output, self)

    def create_request(self, process_id, post_id, user_id):
        '''
        创建请求以及请求对应状态的相关动作
        '''

        # 获取“开始”状态ID

        state_type = 'start_{0}'.format(process_id)
        cur_state = MState.get_by_state_type(state_type)
        if cur_state:
            # 创建请求
            req_id = MRequest.create(process_id, post_id, user_id, cur_state.uid)

            # 创建请求操作
            cur_actions = MTransitionAction.query_by_pro_state(process_id, cur_state.uid)
            act_arr = []
            for cur_act in cur_actions:
                MRequestAction.create(req_id, cur_act['action'], cur_act['transition'])
                act = MAction.get_by_id(cur_act['action']).get()
                if act.action_type.startswith('restart'):
                    act_arr.append({"act_name": act.name, "act_uid": cur_act['action'], "request_id": req_id,
                                    "state_id": cur_state.uid, "process_id": process_id})
            return act_arr, req_id

    def rovoke(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)[0]

        post_id = post_data['post_id']
        user_id = post_data['user_id']

        req = MRequest.query_by_postid(post_id)

        if user_id == str(req.user):
            MRequestAction.update_by_request(req.uid)

        output = {'act_arr': ''}

        return json.dump(output, self)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def amis_submit_action(self, **kwargs):

        post_data = json.loads(self.request.body)

        request_id = post_data['request_id']
        post_id = post_data['post_id']
        user_id = post_data['user_id']
        act_id = post_data['act_id']
        state_id = post_data['state_id']
        process_id = post_data['process_id']

        act_arr = []
        if request_id:
            print("1-" * 50)
            print(act_id)
            print(request_id)

            # 提交的Action与其中一个（is_active = true）的活动RequestActions匹配，设置 is_active = false 和 is_completed = true
            reqact = MRequestAction.get_by_action_request(act_id, request_id)

            if reqact.is_active:
                # 更新操作动态
                print("gengxin")
                MRequestAction.update_by_action(act_id, request_id)

                # 查询该请求中该转换的所有动作是否都为True
                istrues = MRequestAction.query_by_request_trans(request_id, reqact.transition)

                if istrues:
                    if istrues.is_complete:
                        print("1.12 " * 50)
                        # 禁用该请求下其它动作
                        MRequestAction.update_by_action_reqs(act_id, request_id)
                        # 转到下一状态
                        trans = MTransition.get_by_uid(reqact.transition).get()
                        new_state = MState.get_by_uid(trans.next_state).get()

                        if new_state.state_type.startswith('complete'):
                            print("1.13 " * 50)
                            MPost.update_valid(post_id)

                            output = {"responseStatus": 0,
                                      "responseData": {
                                          'act_arr': ''
                                      },
                                      "responseMsg": "ok"
                                      }
                            return json.dump(output, self)
                        else:
                            print("1.14 " * 50)
                            # 创建请求
                            new_request_id = MRequest.create(process_id, post_id, user_id, new_state.uid)

                            # 创建请求操作
                            cur_actions = MTransitionAction.query_by_pro_state(process_id, new_state.uid)

                            for cur_act in cur_actions:
                                MRequestAction.create(new_request_id, cur_act['action'], cur_act['transition'])
                                act = MAction.get_by_id(cur_act['action']).get()

                                act_arr.append(
                                    {"act_name": act.name, "act_uid": cur_act['action'], "request_id": new_request_id,
                                     "cur_state": new_state.uid, "process_id": process_id})

                            output = {"responseStatus": 0,
                                      "responseData": {
                                          'act_arr': act_arr
                                      },
                                      "responseMsg": "ok"
                                      }
                            return json.dump(output, self)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def list(self, kind):

        post_data = self.request.arguments  # {'page': [b'1'], 'perPage': [b'10']}

        page = int(post_data['page'][0].decode('utf-8'))
        perPage = int(post_data['perPage'][0].decode('utf-8'))

        def get_pager_idx():
            '''
            Get the pager index.
            '''

            current_page_number = 1
            if page == '':
                current_page_number = 1
            else:
                try:
                    current_page_number = int(page)
                except TypeError:
                    current_page_number = 1
                except Exception as err:
                    print(err.args)
                    print(str(err))
                    print(repr(err))

            current_page_number = 1 if current_page_number < 1 else current_page_number
            return current_page_number

        current_page_num = get_pager_idx()

        recs = MPost.query_pager_by_slug(kind, current_page_num, perPage)
        # 分类筛选用以下方法
        # recs = MPost.query_list_pager(kind, current_page_num, perPage)

        rec_arr = []

        for rec in recs:
            print("9" * 50)
            print(rec.uid)
            ##查询当前流程的请求
            request_rec = MRequest.query_by_postid(rec.uid)

            if request_rec:
                act_recs = MTransitionAction.query_by_pro_state(request_rec.process, request_rec.current_state)
                act_arr = []
                for act in act_recs:
                    # 判断动作is_active是否是True
                    reqact_rec = MRequestAction.get_by_action_request(act['action'], request_rec.uid)
                    if reqact_rec and reqact_rec.is_active:
                        act_rec = MAction.get_by_id(act['action']).get()

                        # 当前登录用户具有的权限
                        perms = MStaff2Role.query_permissions(self.userinfo.uid)

                        # 当前动作需要的权限
                        per_act_recs = MPermissionAction.query_by_action(act_rec.uid)
                        cur_user_per = []
                        for key in perms:
                            cur_user_per.append(key['permission'])

                        for per_act in per_act_recs:

                            if (str(per_act.permission) in cur_user_per) and (self.userinfo.extinfo.get(f'_per_{per_act.permission}', 0) == 1):
                                act_dic = {"act_name": act_rec.name, "act_uid": act_rec.uid,
                                           "request_id": request_rec.uid,
                                           "state_id": request_rec.current_state_id,
                                           "process_id": request_rec.process_id}
                                act_arr.append(act_dic)

                if act_arr:
                    rec_arr.append(
                        {
                            "uid": rec.uid,
                            "title": rec.title,
                            "cnt_md": rec.cnt_md,
                            "cnt_html": tornado.escape.xhtml_unescape(rec.cnt_html),
                            "user_name": rec.user_name,
                            "keywords": rec.keywords,
                            "logo": rec.logo,
                            "kind": rec.kind,
                            "state": rec.state,
                            "time_create": tools.format_time(rec.time_create),
                            "time_update": tools.format_time(rec.time_update),
                            "view_count": rec.view_count,
                            "rating": rec.rating,
                            "valid": rec.valid,
                            "order": rec.order,
                            "extinfo": rec.extinfo,
                            "router": post_cfg[kind]['router'],
                            "cur_user_id": self.userinfo.uid,
                            "action_arr": act_arr

                        }
                    )

        output = {
            "ok": True,
            "status": 0,
            "msg": "ok",
            "data": {"count": len(rec_arr), "rows": rec_arr}
        }
        return json.dump(output, self, ensure_ascii=False)

    @tornado.web.authenticated
    @privilege.permission(action='can_delete')
    def delete(self, del_id):
        '''
        Delete the post, but return the JSON.
        '''

        current_infor = MPost.get_by_uid(del_id)
        is_deleted = MPost.delete(del_id)
        MCategory.update_count(current_infor.extinfo['def_cat_uid'])
        if is_deleted:
            output = {
                "ok": True,
                "status": 0,
                "msg": "删除成功"
            }
        else:
            output = {
                "ok": True,
                "status": 0,
                "msg": "删除失败"
            }
        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='can_delete')
    @tornado.web.authenticated
    def batch_delete(self, del_id):
        '''
        Delete a link by id.
        '''

        del_uids = del_id.split(",")
        for del_id in del_uids:
            current_infor = MPost.get_by_uid(del_id)
            is_deleted = MPost.delete(del_id)
            MCategory.update_count(current_infor.extinfo['def_cat_uid'])
            if is_deleted:
                output = {
                    "ok": True,
                    "status": 0,
                    "msg": "删除成功"
                }
            else:
                output = {
                    "ok": True,
                    "status": 0,
                    "msg": "删除失败"
                }

        return json.dump(output, self, ensure_ascii=False)
