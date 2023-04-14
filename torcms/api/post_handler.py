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
from torcms.model.state_model import MState, MProcess, MTransition, MRequest, MAction, MRequestAction, \
    MTransitionAction, MStateAction


class ApiPostHandler(PostHandler):
    '''
    Handler of Posts via Ajax.
    '''

    def initialize(self, **kwargs):
        super().initialize()
        self.kind = '1'

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
        elif url_arr[0] == 'submit_state':
            self.submit_state(url_arr[1], url_arr[2], url_arr[3])
        elif url_arr[0] == 'submit_action':
            self.submit_action()

        elif url_arr[0] == 'batch_delete':
            self.batch_delete(url_arr[1])

        else:
            self.redirect('misc/html/404.html')

    def submit_action(self):

        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)[0]

        request_id = post_data['request_id']
        state_id = post_data['state_id']
        post_id = post_data['post_id']
        user_id = post_data['user_id']
        act_id = post_data['act_id']
        pro_id = post_data['pro_id']


        # 更新操作动态
        MRequestAction.update_by_action(act_id, request_id)


        # 查询该请求中该转换的所有动作是否都为True
        trans=MRequestAction.query_by_action_request(act_id,request_id)

        #转到下一状态
        MTransition.query_by_state(state_id)



        for is_active in isactives:
            print(is_active.uid, is_active.action, is_active.is_active, is_active.is_complete)
        istrans = True
        output = {'state': state_id, 'trans_id': trans_id}
        if istrans:
            return json.dump(output, self)
        else:
            return False
    def submit_state(self, post_id, pro_id,state_id):
        request_id = MRequest.create(pro_id, post_id, self.userinfo.uid)
        cur_actions=MTransitionAction.query_by_action(pro_id,state_id)
        for cur_act in cur_actions:

            MRequestAction.create(request_id, cur_act['action'], cur_act['transition'])

        act_recs = MStateAction.query_by_state(state_id)

        act_arr = []
        for act in act_recs:
            act_dic = {"act_name": act['name'], "act_uid": act['uid'], "state": act['state']}
            act_arr.append(act_dic)
        # 以上创建步骤已完成
        istrans = True
        output = {'act_recs': act_arr,"request_id":request_id}

        if istrans:
            return json.dump(output, self)
        else:
            return False

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
        counts = MPost.total_number(kind)
        rec_arr = []

        for rec in recs:
            request_rec = ''
            # request_rec = MRequest.get_id_by_username(rec.uid, rec.user_name)

            # 审核状态#
            exe_actions = MRequestAction.query_by_postid(rec.uid)

            action_arr = []
            for exe_action in exe_actions:
                action_arr = []
                act_recs = MStateAction.query_by_state(exe_action['current_state'])

                for act_rec in act_recs:
                    act = MAction.query_by_id(act_rec.action).get()

                    action_arr.append(act.name)
            # 审核状态#

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
                    "state_request_id": 'request_rec.uid',
                    "action_arr": action_arr
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
