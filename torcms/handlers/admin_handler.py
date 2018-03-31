# -*- coding:utf-8 -*-
'''
Admin
'''
import tornado.web
import config
from torcms.core.base_handler import BaseHandler


class AdminHandler(BaseHandler):
    '''
    Handler for Admin.
    '''

    def initialize(self, **kwargs):
        super(AdminHandler, self).initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        if url_str == '':
            self.index()
        else:
            self.render('misc/html/404.html',
                        kwd={},
                        userinfo=self.userinfo)

    @tornado.web.authenticated
    def index(self):
        self.render('admin/admin_index.html',
                    userinfo=self.userinfo,
                    kwd={},
                    cfg=config.CMS_CFG,
                    router_post=config.router_post)
