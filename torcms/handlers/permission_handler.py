# -*- coding:utf-8 -*-
'''
Handler for links.
'''

import json

import tornado.escape
import tornado.web

from config import CMS_CFG
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.model.permission_model import MPermission


class PermissionHandler(BaseHandler):
    '''
    Handler for links.
    '''

    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_str == 'list':
            self.recent()
        elif url_arr[0] == 'get':
            self.get_by_id(url_arr[1])

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
            self.per_add()
        elif url_arr[0] == '_delete':
            self.delete_by_id(url_arr[1])
        else:
            self.redirect('misc/html/404.html')

    def get_by_id(self, uid):
        rec = MPermission.get_by_uid(uid)
        dic = [{
            "uid": rec.uid,
            "name": rec.name,
            'action': rec.action,
            'controller': rec.controller
        }]

        out_dict = {
            'title': '权限详情',
            'permore_table': dic
        }

        return json.dump(out_dict, self, ensure_ascii=False)

    def recent(self):
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
        recs = MPermission.query_all(current_page_num, perPage)
        counts = MPermission.get_counts()
        for rec in recs:
            dic = {
                "uid": rec.uid,
                "name": rec.name,
                'action': rec.action,
                'controller': rec.controller
            }
            dics.append(dic)
        out_dict = {

            "ok": True,
            "status": 0,
            "msg": "ok",
            'data': {"count": counts,
                     "rows": dics
                     }
        }

        return json.dump(out_dict, self, ensure_ascii=False)

    @tornado.web.authenticated
    def update(self, uid):
        '''
        Update the link.
        '''

        post_data = json.loads(self.request.body)

        if MPermission.update(uid, post_data):
            output = {
                'addinfo ': 1,
            }
        else:
            output = {
                'addinfo ': 0,
            }
        return json.dump(output, self)

    @tornado.web.authenticated
    def per_add(self):
        '''
        user add link.
        '''

        post_data = json.loads(self.request.body)

        cur_uid = tools.get_uudd(2)
        while MPermission.get_by_uid(cur_uid):
            cur_uid = tools.get_uudd(2)

        if MPermission.add_or_update(cur_uid, post_data):
            output = {
                'addinfo ': 1,
            }
        else:
            output = {
                'addinfo ': 0,
            }
        return json.dump(output, self)

    @tornado.web.authenticated
    def delete_by_id(self, del_id):
        '''
        Delete a link by id.
        '''

        if MPermission.delete(del_id):
            output = {'del_link': 1}
        else:
            output = {'del_link': 0}
        return json.dump(output, self)
