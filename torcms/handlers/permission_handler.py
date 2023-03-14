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
        elif url_arr[0] in ['delete', '_delete']:
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

        elif url_arr[0] =='_add':
            self.per_add()
        else:
            self.redirect('misc/html/404.html')

    def recent(self):
        '''
        Recent links.
        '''
        kwd = {
            'pager': '',
            'title': '最近文档',
        }

        
        self.render('admin/permission/list.html',
                    kwd=kwd,
                    view=MPermission.query_link(),
                    format_date=tools.format_date,
                    userinfo=self.userinfo)
       

 

    @tornado.web.authenticated
    def update(self, uid):
        '''
        Update the link.
        '''
        if self.userinfo.role[1] >= '3':
            pass
        else:
            return False
        post_data = self.get_request_arguments()

        post_data['user_name'] = self.get_current_user()
 
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
        if self.check_post_role()['ADD']:
            pass
        else:
            return False
        post_data = self.get_request_arguments()

        post_data['user_name'] = self.get_current_user()

        cur_uid = tools.get_uudd(2)
        while MPermission.get_by_uid(cur_uid):
            cur_uid = tools.get_uudd(2)

        if MPermission.create_link(cur_uid, post_data):
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
        if self.check_post_role()['DELETE']:
            pass
        else:
            return False
       
        if MPermission.delete(del_id):
            output = {'del_link': 1}
        else:
            output = {'del_link': 0}
        return json.dump(output, self)
        

 