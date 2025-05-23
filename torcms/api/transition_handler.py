# -*- coding:utf-8 -*-
'''
Handler for links.
'''

import json

import tornado.web

from torcms.core import privilege, tools
from torcms.core.base_handler import BaseHandler
from torcms.model.process_model import (
    MProcess,
    MRequestAction,
    MState,
    MTransition,
    MTransitionAction,
)


class TransitionHandler(BaseHandler):
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

        if url_arr[0] == '_delete':
            self.delete(url_arr[1]),

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

        parentId = post_data['process'][0].decode('utf-8')

        dics = []
        recs = MTransition.query_by_proid(parentId)

        for rec in recs:
            cur_state = MState.get_by_uid(rec.current_state).get()
            next_state = MState.get_by_uid(rec.next_state).get()
            cur_state_pro = MProcess.get_by_uid(cur_state.process).get()
            next_state_pro = MProcess.get_by_uid(next_state.process).get()

            trans_name = (
                cur_state.name
                + ' ['
                + cur_state_pro.name
                + '] - '
                + next_state.name
                + ' ['
                + next_state_pro.name
                + ']'
            )

            dic = {"label": trans_name, "value": rec.uid}

            dics.append(dic)

        out_dict = {"ok": True, "status": 0, 'data': dics}

        return json.dump(out_dict, self, ensure_ascii=False)

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
        recs = MTransition.query_all_parger(current_page_num, perPage)
        counts = MTransition.get_counts()

        for rec in recs:
            process = MProcess.get_by_uid(rec.process).get()
            cur_state = MState.get_by_uid(rec.current_state).get()
            next_state = MState.get_by_uid(rec.next_state).get()

            cur_state_pro = MProcess.get_by_uid(cur_state.process).get()
            next_state_pro = MProcess.get_by_uid(next_state.process).get()
            dic = {
                "uid": rec.uid,
                "current_state": cur_state.name + ' [' + cur_state_pro.name + '] ',
                "next_state": next_state.name + ' [' + next_state_pro.name + '] ',
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
    def add(self):
        '''
        user add link.
        '''

        post_data = json.loads(self.request.body)
        cur_state = post_data['current_state']
        next_state = post_data['next_state']
        if 'process' in post_data:
            pass
        else:
            return False

        process = post_data["process"]
        exis_rec = MTransition.get_by_cur_next(process, cur_state, next_state)
        if exis_rec.count() > 0:
            output = {"ok": False, "status": 404, "msg": "该流程下已存在当前转换，添加失败"}

        else:
            state_uid = MTransition.create(process, cur_state, next_state)
            if state_uid:
                output = {"ok": True, "status": 0, "msg": "添加转换成功"}
            else:
                output = {"ok": False, "status": 404, "msg": "添加转换失败"}

        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def delete(self, trans_id):
        '''
        delete user by ID.
        '''
        MTransitionAction.delete_by_trans(trans_id)
        MRequestAction.delete_by_trans(trans_id)

        if MTransition.delete(trans_id):
            output = {"ok": True, "status": 0, "msg": "删除转换成功"}
        else:
            output = {"ok": False, "status": 404, "msg": "删除转换失败"}

        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def batch_delete(self, strans_ids):
        '''
        Delete a link by id.
        '''

        del_uids = strans_ids.split(",")
        for trans_id in del_uids:
            MTransitionAction.delete_by_trans(trans_id)
            MRequestAction.delete_by_trans(trans_id)

            if MTransition.delete(trans_id):
                output = {"ok": True, "status": 0, "msg": "删除转换成功"}
            else:
                output = {"ok": False, "status": 404, "msg": "删除转换失败"}

        return json.dump(output, self, ensure_ascii=False)
