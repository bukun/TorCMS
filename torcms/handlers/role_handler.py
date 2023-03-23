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
        elif url_arr[0] == 'chainedOptions':
            self.chainedOptions()
        elif url_arr[0] == 'getpid':
            self.getpid()


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
            self.delete_by_id(url_arr[1])
        elif url_arr[0] == '_add':
            self.per_add()
        elif url_arr[0] == 'batch_edit':
            self.batch_edit()

        else:
            self.redirect('misc/html/404.html')

    def getpid(self):

        dics = []
        recs = MRole.getpid()

        for rec in recs:
            dic = {
                "label": rec.name,
                "value": rec.uid

            }

            dics.append(dic)
        out_dict = {
            "ok": True,
            "status": 0,
            'data': dics

        }

        return json.dump(out_dict, self, ensure_ascii=False)

    def chainedOptions(self):
        '''
        Recent links.
        '''

        post_data = self.request.arguments  # {'page': [b'1'], 'perPage': [b'10']}
        parentId = str(post_data['parentId'][0])[2:-1]
        if parentId == '':
            parentId = '0000'
        dics = []
        recs = MRole.get_by_pid(parentId)

        for rec in recs:
            dic = {
                "label": rec.name,
                "value": rec.uid

            }

            dics.append(dic)
        out_dict = {
            "ok": True,
            "status": 0,
            'data': dics

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
        recs = MRole.query_all(current_page_num, perPage)
        counts = MRole.get_counts()
        for rec in recs:
            dic = {
                "uid": rec.uid,
                "name": rec.name,
                'status': rec.status,
                'pid': rec.pid,
                'time_create': tools.format_time(rec.time_create),
                'time_update': tools.format_time(rec.time_update)
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

    def get_by_id(self, uid):
        rec = MRole.get_by_uid(uid)

        dic = [{
            "uid": rec.uid,
            "name": rec.name,
            'status': rec.status,
            'pid': rec.pid,
            'time_create': tools.format_time(rec.time_create),
            'time_update': tools.format_time(rec.time_update)
        }]

        out_dict = {
            'title': '分组/角色详情',
            'rolemore_table': dic
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
    def batch_edit(self):
        '''
        Update the link.
        '''

        post_data = json.loads(self.request.body)
        aa = self.request.arguments
        print("*" * 50)
        print(post_data)
        print(aa)
        # if MRole.update(uid, post_data):
        #     output = {
        #         'addinfo ': 1,
        #     }
        # else:
        #     output = {
        #         'addinfo ': 0,
        #     }
        # return json.dump(output, self)

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
