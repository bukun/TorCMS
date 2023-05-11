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
    MTransitionAction, MProcess


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

        # elif url_arr[0] == 'batch_edit':
        #     self.batch_edit()

        elif url_arr[0] == 'submit_action':
            self.submit_action()
        elif url_arr[0] == 'amis_submit_action':
            self.amis_submit_action()

        elif url_arr[0] == 'batch_delete':
            self.batch_delete(url_arr[1])

        else:
            self.redirect('misc/html/404.html')

    def create_request(self, process_id, post_id, user_id):
        '''
        创建请求以及请求对应状态的相关动作
        '''

        # 获取“开始”状态ID

        state_type = 'start_{0}'.format(post_id)
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
                    act_arr.append({"act_name": act.name, "act_uid": cur_act['action'], "request_id": req_id})
            return act_arr, cur_state.uid

    def submit_action(self):

        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)[0]

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
                    print("1.2 " * 50)
                    # 禁用该请求下其它动作
                    MRequestAction.update_by_action_reqs(act_id, request_id)
                    # 转到下一状态
                    trans = MTransition.get_by_uid(reqact.transition).get()
                    new_state = MState.get_by_uid(trans.next_state).get()

                    if new_state.state_type.startswith('complete'):
                        print("1.3 " * 50)
                        MPost.update_valid(post_id)

                        output = {'act_arr': '', "request_id": ''}
                        return json.dump(output, self)
                    else:
                        print("1.4 " * 50)
                        # 创建请求
                        new_request_id = MRequest.create(process_id, post_id, user_id, new_state.uid)

                        # 创建请求操作
                        cur_actions = MTransitionAction.query_by_pro_state(process_id, new_state.uid)

                        for cur_act in cur_actions:
                            MRequestAction.create(new_request_id, cur_act['action'], cur_act['transition'])
                            act = MAction.get_by_id(cur_act['action']).get()
                            # if act.action_type.startswith('restart'):
                            act_arr.append(
                                {"act_name": act.name, "act_uid": cur_act['action'], "request_id": new_request_id})
                        print(act_arr)
                        output = {'act_arr': act_arr, "request_id": new_request_id, "cur_state": new_state.uid}

                        return json.dump(output, self)

                else:

                    print("1.6 " * 50)
                    act = MAction.get_by_id(istrues.action).get()
                    act_arr.append({"act_name": act.name, "act_uid": act.uid, "request_id": request_id})

                    output = {'act_arr': act_arr, "request_id": request_id, "cur_state": state_id}
                    return json.dump(output, self)
            else:

                print("1.5 " * 50)
                act = MAction.get_by_id(istrues.action).get()
                act_arr.append({"act_name": act.name, "act_uid": act.uid, "request_id": request_id})

                output = {'act_arr': act_arr, "request_id": request_id, "cur_state": state_id}
                return json.dump(output, self)

        else:
            print("2-" * 50)
            ##

            act_arr, cur_state_id = self.create_request(process_id, post_id, user_id)

            output = {'act_arr': act_arr, "request_id": request_id, "cur_state": cur_state_id}
            return json.dump(output, self)


    def amis_submit_action(self):


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
                    print("1.2 " * 50)
                    # 禁用该请求下其它动作
                    MRequestAction.update_by_action_reqs(act_id, request_id)
                    # 转到下一状态
                    trans = MTransition.get_by_uid(reqact.transition).get()
                    new_state = MState.get_by_uid(trans.next_state).get()

                    if new_state.state_type.startswith('complete'):
                        print("1.3 " * 50)
                        MPost.update_valid(post_id)

                        output = {'act_arr': '', "request_id": ''}
                        return json.dump(output, self)
                    else:
                        print("1.4 " * 50)
                        # 创建请求
                        new_request_id = MRequest.create(process_id, post_id, user_id, new_state.uid)

                        # 创建请求操作
                        cur_actions = MTransitionAction.query_by_pro_state(process_id, new_state.uid)

                        for cur_act in cur_actions:
                            MRequestAction.create(new_request_id, cur_act['action'], cur_act['transition'])
                            act = MAction.get_by_id(cur_act['action']).get()
                            # if act.action_type.startswith('restart'):
                            act_arr.append(
                                {"act_name": act.name, "act_uid": cur_act['action'], "request_id": new_request_id})
                        print(act_arr)
                        output = {'act_arr': act_arr, "request_id": new_request_id, "cur_state": new_state.uid}

                        return json.dump(output, self)

                else:

                    print("1.6 " * 50)
                    act = MAction.get_by_id(istrues.action).get()
                    act_arr.append({"act_name": act.name, "act_uid": act.uid, "request_id": request_id})

                    output = {'act_arr': act_arr, "request_id": request_id, "cur_state": state_id}
                    return json.dump(output, self)
            else:

                print("1.5 " * 50)
                act = MAction.get_by_id(istrues.action).get()
                act_arr.append({"act_name": act.name, "act_uid": act.uid, "request_id": request_id})

                output = {'act_arr': act_arr, "request_id": request_id, "cur_state": state_id}
                return json.dump(output, self)

        else:
            print("2-" * 50)
            ##

            act_arr, cur_state_id = self.create_request(process_id, post_id, user_id)

            output = {'act_arr': act_arr, "request_id": request_id, "cur_state": cur_state_id}
            return json.dump(output, self)

    def list(self, kind):

        post_data = self.request.arguments  # {'page': [b'1'], 'perPage': [b'10']}
        page = int(str(post_data['page'][0])[2:-1])
        perPage = int(str(post_data['perPage'][0])[2:-1])

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
        counts = recs.count()
        rec_arr = []

        for rec in recs:
            cur_pro = MProcess.query_by_name(rec.uid)



            act_arr = []
            if cur_pro.count() > 0:
                process_id = cur_pro.get().uid

                ##查询当前用户的请求
                request_rec = MRequest.get_by_pro(process_id)

                if request_rec:
                    print(request_rec.uid)
                    cur_state_id = request_rec.current_state
                    cur_state = MState.get_by_uid(cur_state_id).get()
                    print(cur_state.state_type)
                    act_id = MAction.get_by_action_type('approve_' + rec.uid)
                    req_act = MRequestAction.get_by_action_request(act_id, request_rec.uid)
                    if req_act:
                        if req_act.is_complete:
                            pass

                        else:
                            act_recs = MTransitionAction.query_by_pro_state(process_id, cur_state_id)

                            for act in act_recs:
                                print("1" * 50)
                                print(act)
                                act_rec = MAction.get_by_id(act['action']).get()
                                act_dic = {"act_name": act_rec.name, "act_uid": act_rec.uid,
                                           "request_id": request_rec.uid,"cur_state_id":  cur_state.uid, "process_id": process_id}
                                act_arr.append(act_dic)
                    else:
                        act_recs = MTransitionAction.query_by_pro_state(process_id, cur_state_id)

                        for act in act_recs:

                            act_rec = MAction.get_by_id(act['action']).get()
                            act_dic = {"act_name": act_rec.name, "act_uid": act_rec.uid, "request_id":  request_rec.uid,
                                       "cur_state_id": cur_state.uid, "process_id": process_id}
                            act_arr.append(act_dic)

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
                "data": {"count": counts, "rows": rec_arr}
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
