# -*- coding:utf-8 -*-
'''
CRUD for the category.
'''

import json

import tornado.web

import config
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost


class CategoryAjaxHandler(BaseHandler):
    '''
    Handler for category.
    '''

    def initialize(self, **kwargs):
        super().initialize()
        self.tmpl_router = 'category_ajax'

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 2:
            if url_arr[1] == 'list':
                self.list_catalog(url_arr[0])
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
            self.add()
        else:
            self.redirect('misc/html/404.html')

    def list_catalog(self, kind):
        '''
        listing the category.
        '''
        kwd = {
            'pager': '',
            'title': '最近文档',
            'kind': kind,
            'router': config.router_post[kind]
        }
        self.render('admin/{0}/category_list.html'.format(self.tmpl_router),
                    kwd=kwd,
                    view=MCategory.query_all(kind),
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    cfg=config.CMS_CFG)

    @tornado.web.authenticated
    def add(self):
        '''
        user add category.
        '''
        if self.check_post_role()['ADD']:
            pass
        else:
            return False
        post_data = self.get_request_arguments()

        post_data['user_name'] = self.get_current_user()

        cur_uid = post_data['uid']

        if MCategory.add_or_update(cur_uid, post_data):

            output = {
                'addinfo ': 1,
            }
        else:
            output = {
                'addinfo ': 0,
            }
        return json.dump(output, self)

    @tornado.web.authenticated
    def update(self, uid):
        '''
        Update the category.
        '''
        if self.check_post_role()['EDIT']:
            pass
        else:
            return False
        post_data = self.get_request_arguments()

        post_data['user_name'] = self.get_current_user()

        if MCategory.update(uid, post_data):
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
        Delete  by id.

        '''
        print("-" * 50)
        print(del_id)
        if self.check_post_role()['DELETE']:
            pass
        else:
            return False
        post_resc = MPost2Catalog.query_postinfo_by_cat(del_id)
        for post in post_resc:
            MPost2Catalog.remove_relation(post.uid, del_id)
        if MCategory.delete(del_id):
            output = {'del_link': 1}
        else:
            output = {'del_link': 0}
        return json.dump(output, self)
