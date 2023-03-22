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
from torcms.model.role_model import MRole


class RoleHandler(BaseHandler):
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
        elif url_arr[0] == '_delete':
            self.delete_by_id(url_arr[1])
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
        else:
            self.redirect('misc/html/404.html')

    def recent(self):
        '''
        Recent links.
        '''
        dics = []
        recs = MRole.query_all()
        for rec in recs:
            dic = {
                "uid": rec.uid,
                "name": rec.name,
                'status': rec.status,
                'pid':rec.pid,
                'time_create': tools.format_time(rec.time_create),
                'time_update': tools.format_time(rec.time_update)
            }
            dics.append(dic)
        out_dict = {
            'title': '分组/角色列表',
            'rolelist_table': dics
        }

        return json.dump(out_dict, self, ensure_ascii=False)
    def get_by_id(self,uid):
        rec = MRole.get_by_uid(uid)
        dic = {
            "uid": rec.uid,
            "name": rec.name,
            'status': rec.status,
            'pid': rec.pid,
            'time_create': tools.format_time(rec.time_create),
            'time_update': tools.format_time(rec.time_update)
        }


        out_dict = {
            'title': '分组/角色列表',
            'rolelist_table': dic
        }

        return json.dump(out_dict, self, ensure_ascii=False)

    @tornado.web.authenticated
    def update(self, uid):
        '''
        Update the link.
        '''

        post_data = json.loads(self.request.body)


        if MRole.update(uid, post_data):
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
        while MRole.get_by_uid(cur_uid):
            cur_uid = tools.get_uudd(2)

        if MRole.add_or_update(cur_uid, post_data):
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

        if MRole.delete(del_id):
            output = {'del_link': 1}
        else:
            output = {'del_link': 0}
        return json.dump(output, self)
