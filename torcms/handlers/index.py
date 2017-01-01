# -*- coding:utf-8 -*-
'''
Index for the application.
'''


import tornado.escape
import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.model.category_model import MCategory
from torcms.model.link_model import MLink
from torcms.model.page_model import MPage
from torcms.model.post_model import MPost
from config import cfg


class IndexHandler(BaseHandler):
    '''
    Index for the application.
    '''

    def initialize(self):
        super(IndexHandler, self).initialize()
        self.mpost = MPost()
        self.mcat = MCategory()
        self.mpage = MPage()
        self.mlink = MLink()

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get(self, *args, **kwargs):
        if len(args) == 0:
            self.index()
        else:
            self.render('html/404.html', kwd={}, userinfo=self.userinfo)

    def index(self):
        '''
        Index funtion.
        :return:
        '''
        kwd = {
            # 'cookie_str': cstr
        }
        self.render('index/index.html',
                    userinfo=self.userinfo,
                    catalog_info=self.mcat.query_all(by_order=True),
                    link=self.mlink.query_all(),
                    unescape=tornado.escape.xhtml_unescape,
                    cfg=cfg,
                    view=self.mpost.query_most_pic(20),
                    kwd=kwd, )

