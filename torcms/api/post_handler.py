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
from torcms.model.state_model import MState, MProcess, MTransition, MRequest, MAction, MRequestAction, MTransitionAction


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
            self.submit_state(url_arr[1], url_arr[2])

        elif url_arr[0] == 'batch_delete':
            self.batch_delete(url_arr[1])

        else:
            self.redirect('misc/html/404.html')

    def submit_state(self, post_id, state):

        state_init_dics = [
            {"name": "start", "state_type": "start",
             "description": "开始审核:每个进程只应该一个。此状态是创建新请求时所处的状态",
             "action": [
                 {"name": "approve", "action_type": "approve", "description": "操作人将请求应移至下一个状态"},
                 {"name": "deny", "action_type": "deny", "description": "操作人将请求应移至上一个状态"},
                 {"name": "cancel", "action_type": "cancel", "description": "操作人将请求应在此过程中移至“已取消”状态"}
             ]
             },

            {"name": "complete", "state_type": "complete",
             "description": "完成:表示此状态下的任何请求已正常完成的状态",
             "action": [
                 {"name": "resolve", "action_type": "resolve", "description": "操作人将将请求一直移动到Completed状态"},
             ]
             },
            {"name": "denied", "state_type": "denied",
             "description": "拒绝:表示此状态下的任何请求已被拒绝的状态（例如，从未开始且不会被处理）",
             "action": [
                 {"name": "deny", "action_type": "deny", "description": "操作人将请求应移至上一个状态"},
                 {"name": "restart", "action_type": "restart", "description": "操作人将将请求移回到进程中的“开始”状态"},
                 {"name": "cancel", "action_type": "cancel", "description": "操作人将请求应在此过程中移至“已取消”状态"}
             ]
             },
            {"name": "cancelled", "state_type": "cancelled",
             "description": "取消:表示此状态下的任何请求已被取消的状态（例如，工作已开始但尚未完成）",
             "action": [{"name": "restart", "action_type": "restart",
                         "description": "操作人将将请求移回到进程中的“开始”状态"}]

             }
        ]

        # process
        pro_id = MProcess.create(state + '_' + post_id)
        if pro_id:
            pass
        else:
            return False

        # state
        state_get_dics = {}
        cur_action_arr = []
        for state_dic in state_init_dics:
            post_data = {
                "process": pro_id,
                "name": state_dic['name'] + '_{0}'.format(post_id),
                "state_type": state_dic['state_type'] + '_{0}'.format(post_id),
                "description": state_dic['description'] + '_{0}'.format(post_id)
            }

            state_get_dics = MState.create(post_data, state_get_dics)
            if state_get_dics:
                pass
            else:
                return False

            # Action
            for action_dic in state_dic['action']:
                action = {
                    "process": pro_id,
                    "name": action_dic['name'] + '_{0}'.format(post_id),
                    "action_type": action_dic['action_type'] + '_{0}'.format(post_id),
                    "description": action_dic['description']  + '_{0}'.format(post_id)
                }

                cur_action_arr = MAction.create(pro_id, action, cur_action_arr)



        # request
        request_id = MRequest.create(pro_id, post_id, self.userinfo.uid)

        # Transition
        cur_state_id = state_get_dics['{0}_{1}'.format(state, post_id)]
        state_start_id = state_get_dics['start_{0}'.format(post_id)]
        state_com_id = state_get_dics['complete_{0}'.format(post_id)]
        state_denied_id = state_get_dics['denied_{0}'.format(post_id)]
        state_cancelled_id = state_get_dics['cancelled_{0}'.format(post_id)]

        if state == 'start':
            next_static = {state_com_id, state_denied_id, state_cancelled_id}
        elif state == 'denied':
            next_static = {state_start_id}
        elif state == 'cancelled':
            next_static = {state_com_id, state_denied_id}
        else:
            next_static = {}

        istrans = False
        if next_static:
            for next_state in next_static:
                trans_rec = MTransition.create(pro_id, cur_state_id, next_state)

                # TransitionAction
                # MTransitionAction.create(trans_id, cur_act_id)
                # RequestActions
                for cur_act_id in cur_action_arr:
                    istrans = MRequestAction.create(request_id, cur_act_id, trans_rec.uid)

        # 以上创建步骤已完成

        output = {'state': state, 'process_id': pro_id}
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
            request_rec = MRequest.get_id_by_username(rec.uid, rec.user_name)

            # 审核状态#
            exe_actions = MRequestAction.query_by_postid(rec.uid)
            print("*" * 50)

            for exe_action in exe_actions:
                action_arr = []
                act_recs = MAction.query_by_proid(exe_action['process'])
                for act_rec in act_recs:
                    action_arr.append({act_rec.uid: act_rec.name})
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
                    "state_request_id": request_rec.uid,
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
