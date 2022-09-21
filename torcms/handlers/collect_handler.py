# -*- coding:utf-8 -*-
'''
For User collection
'''

import json

import tornado.web

from config import CMS_CFG
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.core.tools import logger
from torcms.model.collect_model import MCollect


class CollectHandler(BaseHandler):
    '''
    For User collection
    '''

    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        if url_str:
            url_arr = self.parse_url(url_str)
        else:
            return False
        if len(url_arr) == 1:
            if url_str == 'list':
                self.show_list(url_str)
            else:
                if self.get_current_user():
                    self.add_or_update(url_str)
                else:
                    self.set_status(403)
                    return False
        elif len(url_arr) == 2:
            if url_arr[0] == 'remove':
                self.remove_collect(url_arr[1])
            else:
                self.show_list(url_arr[0], url_arr[1])

    @tornado.web.authenticated
    def add_or_update(self, app_id):
        '''
        Add or update the category.
        '''
        logger.info('Collect info: user-{0}, uid-{1}'.format(
            self.userinfo.uid, app_id))
        MCollect.add_or_update(self.userinfo.uid, app_id)
        out_dic = {'success': True}
        return json.dump(out_dic, self)

    @tornado.web.authenticated
    def remove_collect(self, post_id):
        '''
        Add or update the category.
        '''
        logger.info('Collect info: user-{0}, uid-{1}'.format(
            self.userinfo.uid, post_id))
        MCollect.remove_collect(self.userinfo.uid, post_id)
        out_dic = {'success': True}
        return json.dump(out_dic, self)

    @tornado.web.authenticated
    def show_list(self, the_list, cur_p=''):
        '''
        List of the user collections.
        '''

        current_page_number = 1
        if cur_p == '':
            current_page_number = 1
        else:
            try:
                current_page_number = int(cur_p)
            except TypeError:
                current_page_number = 1
            except Exception as err:
                print(err.args)
                print(str(err))
                print(repr(err))

        current_page_number = 1 if current_page_number < 1 else current_page_number

        num_of_cat = MCollect.count_of_user(self.userinfo.uid)
        page_num = int(num_of_cat / CMS_CFG['list_num']) + 1

        kwd = {'current_page': current_page_number}

        self.render('misc/collect/list.html',
                    recs_collect=MCollect.query_pager_by_all(
                        self.userinfo.uid, current_page_number).objects(),
                    userinfo=self.userinfo,
                    cfg=CMS_CFG,
                    kwd=kwd)
