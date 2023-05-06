# -*- coding:utf-8 -*-
'''
Handler for links.
'''

import json
import tornado.web
from torcms.core import tools, privilege
from torcms.core.base_handler import BaseHandler
from torcms.model.process_model import MProcess


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

        role_uid = MProcess.create(post_data.get('name'))
        if role_uid:

            output = {
                "ok": True,
                "status": 0,
                "msg": "添加流程成功"
            }
        else:
            output = {
                "ok": False,
                "status": 404,
                "msg": "添加流程失败"
            }
        return json.dump(output, self, ensure_ascii=False)
