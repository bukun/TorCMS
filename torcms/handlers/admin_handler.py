# -*- coding:utf-8 -*-
import tornado.web
import config
from torcms.core.base_handler import BaseHandler


class AdminHandler(BaseHandler):
    def initialize(self):
        super(AdminHandler, self).initialize()

    def get(self, input=''):
        if input == '':
            self.index()
        else:
            self.render('html/404.html',
                        kwd={},
                        userinfo=self.userinfo)

    @tornado.web.authenticated
    def index(self):
        self.render('admin/admin_index.html',
                    userinfo=self.userinfo,
                    kwd={},
                    cfg=config.cfg,
                    )
