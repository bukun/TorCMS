# -*- coding:utf-8 -*-
'''
Handler for links.
'''

import json

import tornado.web

from torcms.core import privilege, tools
from torcms.core.base_handler import BaseHandler
from torcms.model.process_model import (
    MAction,
    MPermissionAction,
    MProcess,
    MRequest,
    MRequestAction,
    MState,
    MTransition,
    MTransitionAction,
)


class ProcessHandler(BaseHandler):
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

        elif url_arr[0] == '_add':
            self.add()
        elif url_arr[0] == '_delete':
            self.delete(url_arr[1])
        elif url_arr[0] == 'batch_delete':
            self.batch_delete(url_arr[1])

        else:
            self.redirect('misc/html/404.html')

    def list(self):
        '''
        Recent links.
        '''

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
        dics = []
        recs = MProcess.query_all_parger(current_page_num, perPage)
        counts = MProcess.get_counts()

        for rec in recs:
            dic = {
                "uid": rec.uid,
                "name": rec.name,
            }

            dics.append(dic)
        out_dict = {
            "ok": True,
            "status": 0,
            "msg": "ok",
            "data": {"count": counts, "rows": dics},
        }

        return json.dump(out_dict, self, ensure_ascii=False)

    def chainedOptions(self):
        '''
        Recent links.
        '''

        dics = []
        recs = MProcess.query_all()

        for rec in recs:
            dic = {"label": rec.name, "value": rec.uid}

            dics.append(dic)
        out_dict = {"ok": True, "status": 0, 'data': dics}

        return json.dump(out_dict, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def update(self, uid):
        '''
        Update the link.
        '''

        post_data = json.loads(self.request.body)

        if MProcess.update(uid, post_data):
            output = {"ok": True, "status": 0, "msg": "更新流程成功"}

        else:
            output = {"ok": False, "status": 404, "msg": "更新流程失败"}

        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def add(self):
        '''
        user add link.
        '''

        post_data = json.loads(self.request.body)

        role_uid = MProcess.create(post_data.get('name'))
        if role_uid:
            output = {"ok": True, "status": 0, "msg": "添加流程成功"}
        else:
            output = {"ok": False, "status": 404, "msg": "添加流程失败"}
        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def delete(self, process_id):
        '''
        Delete a link by id.
        '''
        trans = MTransition.query_by_proid(process_id)

        for tran in trans:
            try:
                MRequestAction.delete_by_trans(tran.uid)
                pass
            except Exception as err:
                print(repr(err))
                pass
            try:
                MTransitionAction.delete_by_trans(tran.uid)
                pass
            except Exception as err:
                print(repr(err))
                pass
            try:
                MTransition.delete(tran.uid)
                pass
            except Exception as err:
                print(repr(err))
                pass

        req_recs = MRequest.get_by_pro(process_id)
        if req_recs:
            for req_rec in req_recs:
                print(req_rec.uid)
                try:
                    MRequest.delete(req_rec.uid)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass

        act_recs = MAction.query_by_proid(process_id)
        if act_recs:
            for act in act_recs:
                try:
                    MPermissionAction.delete_by_action(act.uid)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass
                try:
                    MAction.delete(act.uid)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass

        states = MState.query_by_pro_id(process_id)
        if states:
            for state in states:
                try:
                    MState.delete(state.uid)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass

        if MProcess.delete_by_uid(process_id):
            output = {"ok": True, "status": 0, "msg": "删除流程成功"}
        else:
            output = {"ok": False, "status": 404, "msg": "删除流程失败"}
        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def batch_delete(self, del_id):
        '''
        Delete a link by id.
        '''

        del_uids = del_id.split(",")
        for process_id in del_uids:
            trans = MTransition.query_by_proid(process_id)

            for tran in trans:
                try:
                    MRequestAction.delete_by_trans(tran.uid)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass
                try:
                    MTransitionAction.delete_by_trans(tran.uid)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass
                try:
                    MTransition.delete(tran.uid)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass

            req_recs = MRequest.get_by_pro(process_id)
            if req_recs:
                for req_rec in req_recs:
                    print(req_rec.uid)
                    try:
                        MRequest.delete(req_rec.uid)
                        pass
                    except Exception as err:
                        print(repr(err))
                        pass

            act_recs = MAction.query_by_proid(process_id)
            if act_recs:
                for act in act_recs:
                    try:
                        MPermissionAction.delete_by_action(act.uid)
                        pass
                    except Exception as err:
                        print(repr(err))
                        pass
                    try:
                        MAction.delete(act.uid)
                        pass
                    except Exception as err:
                        print(repr(err))
                        pass

            states = MState.query_by_pro_id(process_id)
            if states:
                for state in states:
                    try:
                        MState.delete(state.uid)
                        pass
                    except Exception as err:
                        print(repr(err))
                        pass

            if MProcess.delete_by_uid(process_id):
                output = {"ok": True, "status": 0, "msg": "删除流程成功"}
            else:
                output = {"ok": False, "status": 404, "msg": "删除流程失败"}

        return json.dump(output, self, ensure_ascii=False)
