# -*- coding:utf-8 -*-

'''
Hander for entiey, such as files or URL.
'''

import tornado.ioloop
import tornado.web

import config
from torcms.core.base_handler import BaseHandler
from torcms.model.entity2user_model import MEntity2User


class Entity2UserHandler(BaseHandler):
    '''
    Hander for entiey, such as files or URL.
    '''

    def initialize(self, **kwargs):
        super(Entity2UserHandler, self).initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        if url_str == 'list' or url_str == '':
            self.list()
        elif len(url_arr) == 1:
            self.list(url_arr[0])
        else:
            self.render('misc/html/404.html', kwd={}, userinfo=self.userinfo)

    @tornado.web.authenticated
    def list(self, cur_p=''):
        '''
        List the entities of the user.
        '''
        current_page_number = int(cur_p) if cur_p else 1
        current_page_number = 1 if current_page_number < 1 else current_page_number

        kwd = {
            'current_page': current_page_number
        }
        recs = MEntity2User.get_all_pager(current_page_num=current_page_number).naive()
        self.render('misc/entity/entity_download.html',
                    imgs=recs,
                    cfg=config.CMS_CFG,
                    kwd=kwd,
                    userinfo=self.userinfo)
