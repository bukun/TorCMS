# -*- coding:utf-8 -*-
'''
Handler for links.
'''

import json
import tornado.web
from torcms.core import tools, privilege
from torcms.core.base_handler import BaseHandler
from torcms.model.process_model import MAction, MTransition, MRequestAction, MTransitionAction, MState,MProcess



class ActionHandler(BaseHandler):
    '''
    Handler for links.
    '''

    def initialize(self, **kwargs):
        super().initialize()
        self.kind = 'u'

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_str == 'list':
            self.list()

        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render(
                'misc/html/404.html',
                kwd=kwd,
                userinfo=self.userinfo,
            )

    def post(self, *args, **kwargs):
        url_str = args[0]

        if url_str == '':
            return
        url_arr = self.parse_url(url_str)

        if url_arr[0] == '_edit':
            self.update(url_arr[1])
        elif url_arr[0] == '_delete':
            self.delete(url_arr[1]),
        elif url_arr[0] == 'batch_edit':
            self.batch_edit()
        elif url_arr[0] == 'batch_delete':
            self.batch_delete(url_arr[1])
        elif url_arr[0] == '_add':
            self.add()


        else:
            self.redirect('misc/html/404.html')

    def list(self):
        '''
        Recent links.
        '''

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
        dics = []
        recs = MAction.query_all_parger(current_page_num, perPage)
        counts = MAction.get_counts()

        for rec in recs:
            process = MProcess.get_by_uid(rec.process).get()
            trans_rec = MTransition.query_by_action(rec.uid, rec.process).get()

            cur_state = MState.get_by_uid(trans_rec.current_state).get()
            next_state = MState.get_by_uid(trans_rec.next_state).get()
            trans_name = cur_state.name + ' - ' + next_state.name

            dic = {
                "uid": rec.uid,
                "name": rec.name,
                "action_type": rec.action_type,
                "description": rec.description,
                "process": process.name,
                "transition": trans_name
            }

            dics.append(dic)
        out_dict = {
            "ok": True,
            "status": 0,
            "msg": "ok",
            "data": {"count": counts, "rows": dics},
        }

        return json.dump(out_dict, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def add(self):
        '''
        user add link.
        '''

        post_data = json.loads(self.request.body)
        if 'transition' in post_data and 'process' in post_data:
            pass
        else:
            return False

        transition = post_data["transition"]
        process = post_data["process"]

        exis_rec = MAction.query_by_pro_actname(transition, post_data['name'])

        if exis_rec.count() > 0:

            output = {
                "ok": False,
                "status": 404,
                "msg": "该流程下已存在当前动作，添加失败"
            }

        else:

            act_uid = MAction.create(process, post_data)
            if act_uid:
                trans_uid = MTransitionAction.create(transition, act_uid)
                if trans_uid:

                    output = {
                        "ok": True,
                        "status": 0,
                        "msg": "添加成功"
                    }
                else:
                    output = {
                        "ok": False,
                        "status": 404,
                        "msg": "该转换下已存在当前动作，添加失败"
                    }
            else:
                output = {
                    "ok": True,
                    "status": 0,
                    "msg": "当前动作已存在,添加动作失败"
                }

        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def update(self, uid):
        '''
        Update the link.
        '''

        post_data = json.loads(self.request.body)

        if 'transition' in post_data and 'process' in post_data:
            pass
        else:
            return False

        transition = post_data["transition"]
        process = post_data["process"]

        exis_rec = MAction.query_by_pro_actname(transition, post_data['name'])
        # trans_extis_rec = MTransitionAction.query_by_trans_act(transition, uid)
        if exis_rec.count() > 0:

            output = {
                "ok": False,
                "status": 404,
                "msg": "该流程下已存在当前动作，修改失败"
            }
        # elif trans_extis_rec.count() > 0:
        #     output = {
        #         "ok": False,
        #         "status": 404,
        #         "msg": "该转换下已存在当前动作，修改失败"
        #     }

        else:

            if MAction.update(uid, post_data) and MAction.update_process(process, uid):
                MTransitionAction.create(transition, uid)
                output = {
                    "ok": True,
                    "status": 0,
                    "msg": "更新动作成功"
                }


            else:
                output = {
                    "ok": False,
                    "status": 404,
                    "msg": "更新动作失败"
                }

        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def batch_edit(self):
        '''
        Update the link.
        '''

        post_data = json.loads(self.request.body)

        ids = post_data.get("ids", "").split(",")
        for uid in ids:

            transition = post_data["transition"]
            process = post_data["process"]

            trans_extis_rec = MTransitionAction.query_by_trans_act(transition, uid)

            if trans_extis_rec.count() > 0:
                output = {
                    "ok": False,
                    "status": 404,
                    "msg": "该转换下已存在当前动作，修改失败"
                }

            else:

                if MAction.update_process(process, uid) and MTransitionAction.update(transition, uid):

                    output = {
                        "ok": True,
                        "status": 0,
                        "msg": "更新流程，转换成功"
                    }


                else:
                    output = {
                        "ok": False,
                        "status": 404,
                        "msg": "更新流程，转换失败"
                    }

        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    def delete(self, action_id):
        '''
        delete user by ID.
        '''
        MTransitionAction.delete_by_actid(action_id)
        MRequestAction.delete_by_actid(action_id)

        if MAction.delete(action_id):
            output = {"ok": True,
                      "status": 0,
                      "msg": "删除动作成功"
                      }
        else:
            output = {
                "ok": False,
                "status": 404,
                "msg": "删除动作失败"
            }

        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def batch_delete(self, act_ids):
        '''
        Delete a link by id.
        '''

        del_uids = act_ids.split(",")
        for action_id in del_uids:
            MTransitionAction.delete_by_actid(action_id)
            MRequestAction.delete_by_actid(action_id)

            if MAction.delete(action_id):
                output = {"ok": True,
                          "status": 0,
                          "msg": "删除动作成功"
                          }
            else:
                output = {
                    "ok": False,
                    "status": 404,
                    "msg": "删除动作失败"
                }

        return json.dump(output, self, ensure_ascii=False)
