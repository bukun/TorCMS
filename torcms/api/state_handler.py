# -*- coding:utf-8 -*-
'''
Handler for links.
'''

import json
import tornado.web
from torcms.core import tools, privilege
from torcms.core.base_handler import BaseHandler
from torcms.model.state_model import MState, MStateAction, MTransition
from torcms.model.role_model import MRole


class StateHandler(BaseHandler):
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
        elif url_arr[0] == 'chainedOptions':
            self.chainedOptions()
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
    def chainedOptions(self):
        '''
        Recent links.
        '''

        post_data = self.request.arguments  # {'page': [b'1'], 'perPage': [b'10']}
        process = str(post_data['pro'][0])[2:-1]
        dics = []
        recs = MState.query_by_pro_id(process)

        for rec in recs:
            dic = {"label": rec.name, "value": rec.uid}

            dics.append(dic)
        out_dict = {"ok": True, "status": 0, 'data': dics}

        return json.dump(out_dict, self, ensure_ascii=False)
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
        recs = MState.query_all_parger(current_page_num, perPage)
        counts = MState.get_counts()

        for rec in recs:
            process = MRole.get_by_uid(rec.process)
            dic = {
                "uid": rec.uid,
                "name": rec.name,
                "state_type": rec.state_type,
                "description": rec.description,
                "process": process.name,
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
    def update(self, uid):
        '''
        Update the link.
        '''

        post_data = json.loads(self.request.body)

        if 'ext_role0' in post_data:
            pass
        else:
            return False

        the_roles_arr = []
        def_roles_arr = ['ext_role{0}'.format(x) for x in range(10)]
        for key in def_roles_arr:
            if key not in post_data:
                continue
            if post_data[key] == '' or post_data[key] == '0':
                continue

            if post_data[key] in the_roles_arr:
                continue

            the_roles_arr.append(post_data[key])

        for process in the_roles_arr:

            rec = MState.query_by_uid(uid).get()
            exis_rec = MState.query_by_pro_name(process, rec.name)

            if exis_rec.count() > 0:
                output = {
                    "ok": False,
                    "status": 404,
                    "msg": "该流程下已存在当前状态，修改失败"
                }
            else:

                post_data["process"] = process
                if MState.update_process(uid, post_data):
                    output = {
                        "ok": True,
                        "status": 0,
                        "msg": "更新流程成功"
                    }

                else:
                    output = {
                        "ok": False,
                        "status": 404,
                        "msg": "更新流程失败"
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
        if 'ext_role0' in post_data:
            pass
        else:
            return False

        the_roles_arr = []
        def_roles_arr = ['ext_role{0}'.format(x) for x in range(10)]
        for key in def_roles_arr:
            if key not in post_data:
                continue
            if post_data[key] == '' or post_data[key] == '0':
                continue

            if post_data[key] in the_roles_arr:
                continue

            the_roles_arr.append(post_data[key])
        for uid in ids:
            for process in the_roles_arr:
                rec = MState.query_by_uid(uid).get()
                exis_rec = MState.query_by_pro_name(process, rec.name)

                if exis_rec.count() > 0:
                    output = {
                        "ok": False,
                        "status": 404,
                        "msg": "该流程下已存在当前状态，修改失败"
                    }
                else:

                    post_data["process"] = process
                    if MState.update_process(uid, post_data):
                        output = {
                            "ok": True,
                            "status": 0,
                            "msg": "更新流程成功"
                        }

                    else:
                        output = {
                            "ok": False,
                            "status": 404,
                            "msg": "更新流程失败"
                        }

        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def add(self):
        '''
        user add link.
        '''

        post_data = json.loads(self.request.body)
        if 'ext_role0' in post_data:
            pass
        else:
            return False

        the_roles_arr = []

        def_roles_arr = ['ext_role{0}'.format(x) for x in range(10)]
        for key in def_roles_arr:
            if key not in post_data:
                continue
            if post_data[key] == '' or post_data[key] == '0':
                continue

            if post_data[key] in the_roles_arr:
                continue

            the_roles_arr.append(post_data[key])

        for process in the_roles_arr:

            post_data["process"] = process

            exis_rec = MState.query_by_pro_name(process, post_data['name'])
            if exis_rec.count() > 0:

                output = {
                    "ok": False,
                    "status": 404,
                    "msg": "该流程下已存在当前状态，添加失败"
                }

            else:
                pro_rec = MRole.get_by_uid(process)
                state_uid = MState.create(post_data,pro_rec.name)
                if state_uid:

                    output = {
                        "ok": True,
                        "status": 0,
                        "msg": "添加状态成功"
                    }
                else:
                    output = {
                        "ok": False,
                        "status": 404,
                        "msg": "添加状态失败"
                    }

        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    def delete(self, state_id):
        '''
        delete user by ID.
        '''
        MStateAction.delete_by_state(state_id)
        MTransition.delete_by_state(state_id)

        if MState.delete(state_id):
            output = {"ok": True,
                      "status": 0,
                      "msg": "删除状态成功"
                      }
        else:
            output = {
                "ok": False,
                "status": 404,
                "msg": "删除状态失败"
            }

        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def batch_delete(self, state_ids):
        '''
        Delete a link by id.
        '''

        del_uids = state_ids.split(",")
        for state_id in del_uids:
            MStateAction.delete_by_state(state_id)
            MTransition.delete_by_state(state_id)

            if MState.delete(state_id):
                output = {"ok": True,
                          "status": 0,
                          "msg": "删除状态成功"
                          }
            else:
                output = {
                    "ok": False,
                    "status": 404,
                    "msg": "删除状态失败"
                }

        return json.dump(output, self, ensure_ascii=False)
