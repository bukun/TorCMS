# -*- coding:utf-8 -*-
'''
Index for the application.
'''

import tornado.escape
import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.model.category_model import MCategory
from torcms.model.link_model import MLink
from torcms.model.post_model import MPost
from config import CMS_CFG


class IndexHandler(BaseHandler):
    '''
    Index for the application.
    '''

    def initialize(self):
        super(IndexHandler, self).initialize()

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get(self, *args):
        if len(args) == 0 or args[0] == 'index':
            self.index()
        else:
            self.render('html/404.html', kwd={}, userinfo=self.userinfo)

    def index(self):
        '''
        Index funtion.
        '''
        self.render('index/index.html',
                    userinfo=self.userinfo,
                    catalog_info=MCategory.query_all(by_order=True),
                    link=MLink.query_all(),
                    unescape=tornado.escape.xhtml_unescape,
                    cfg=CMS_CFG,
                    view=MPost.query_most_pic(20),
                    kwd={}, )
