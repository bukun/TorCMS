# -*- coding:utf-8 -*-

'''
The basic HTML Page handler.
'''

import json

import tornado.escape
import tornado.web

from config import CMS_CFG
from config import router_post
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.core.tools import logger
from torcms.model.category_model import MCategory
from torcms.model.label_model import MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_hist_model import MPostHist
from torcms.model.post_model import MPost
from torcms.model.relation_model import MRelation


class PostListHandler(BaseHandler):
    '''
    The basic HTML Page handler.
    '''

    def initialize(self):
        super(PostListHandler, self).initialize()
        self.kind = '1'

    def get(self, *args):

        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_str == 'recent':
            self.recent()
        elif url_str == '_refresh':
            self.refresh()

        else:
            kwd = {
                'info': '404. Page not found!',
            }
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )



    def recent(self, with_catalog=True, with_date=True):
        '''
        List posts that recent edited.
        :param with_catalog:
        :param with_date:
        :return:
        '''
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': 'Recent posts.',
            'with_catalog': with_catalog,
            'with_date': with_date,
        }
        self.render('post_{0}/post_list.html'.format(self.kind),
                    kwd=kwd,
                    view=MPost.query_recent(num=20, kind=self.kind),
                    postinfo=MPost.query_recent(num=20, kind=self.kind),
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    cfg=CMS_CFG, )



    def refresh(self):
        '''
        List the post of dated.
        :return:
        '''
        kwd = {
            'pager': '',
            'title': '',
        }
        self.render('post_{0}/post_list.html'.format(self.kind),
                    kwd=kwd,
                    userinfo=self.userinfo,
                    view=MPost.query_dated(10),
                    postrecs=MPost.query_dated(10),
                    format_date=tools.format_date,
                    unescape=tornado.escape.xhtml_unescape,
                    cfg=CMS_CFG, )
