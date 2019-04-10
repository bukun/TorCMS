# -*- coding:utf-8 -*-

'''
CRUD for the category.
'''

import json
import tornado.web
import config
from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.category_model import MCategory


class CategoryAjaxHandler(BaseHandler):
    '''
    Handler for category.
    '''

    def initialize(self, **kwargs):
        super(CategoryAjaxHandler, self).initialize()
        self.tmpl_router = 'category_ajax'

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 2:
            if url_arr[1] == 'list':
                self.list_catalog(url_arr[0])

        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo, )

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
                    view=MCategory.query_all(kind, by_order=True),
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    cfg=config.CMS_CFG)
