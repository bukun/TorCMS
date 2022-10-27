# -*- coding:utf-8 -*-
'''
The basic HTML Page handler.
'''

import json
import tornado.gen
import tornado.web
import config
from config import router_post, check_type
from torcms.core import privilege
from torcms.core.base_handler import BaseHandler
from torcms.model.post_model import MPost


class CheckHandler(BaseHandler):

    def initialize(self, **kwargs):
        super(CheckHandler, self).initialize()
        self.is_p = True
        self.kind = kwargs.get('kind', '9')

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_str == 'pend_review':
            self.pend_review(url_str)
        elif url_str == 'publish':
            self.publish_list(url_str)
        elif len(url_arr) == 2:
            if url_arr[0] == 'pend_review':
                self.pend_review(url_arr[0], cur_p=url_arr[1])
            elif url_arr[0] == 'publish':
                self.publish_list(url_arr[0], cur_p=url_arr[1])
        else:
            self.show404()

    @tornado.web.authenticated
    @privilege.auth_check
    def pend_review(self, list, **kwargs):
        '''
        The default page of examine.
        '''

        post_data = self.get_request_arguments()
        state = post_data.get('state', '')
        kind = post_data.get('kind', '9')

        def get_pager_idx():
            '''
            Get the pager index.
            '''
            cur_p = kwargs.get('cur_p')
            the_num = int(cur_p) if cur_p else 1
            the_num = 1 if the_num < 1 else the_num
            return the_num

        current_page_num = get_pager_idx()
        num_of_cat = MPost.count_of_certain_by_state(state, kind)
        tmp_page_num = int(num_of_cat / config.CMS_CFG['list_num'])
        page_num = (tmp_page_num if
                    abs(tmp_page_num - num_of_cat / config.CMS_CFG['list_num'])
                    < 0.1 else tmp_page_num + 1)

        kwd = {
            'current_page': current_page_num,
            'count': num_of_cat,
            'pager_num': page_num,
            'config_num': config.CMS_CFG['list_num'],
            'kind': kind,
            'router': router_post[kind],
            'post_type': check_type[kind]
        }

        res = MPost.query_by_state(state, kind, current_page_num)

        self.render('static_pages/check/pend_review.html',
                    userinfo=self.userinfo,
                    recs=res,
                    kwd=kwd,
                    state=state,

                    )

    @tornado.web.authenticated
    def publish_list(self, list, **kwargs):
        '''
        The default page of examine.
        '''

        post_data = self.get_request_arguments()
        state = post_data.get('state', '')
        kind = post_data.get('kind', '9')

        def get_pager_idx():
            '''
            Get the pager index.
            '''
            cur_p = kwargs.get('cur_p')
            the_num = int(cur_p) if cur_p else 1
            the_num = 1 if the_num < 1 else the_num
            return the_num

        current_page_num = get_pager_idx()
        num_of_cat = MPost.count_of_certain_by_username(self.userinfo.user_name, state, kind)
        tmp_page_num = int(num_of_cat / config.CMS_CFG['list_num'])
        page_num = (tmp_page_num if
                    abs(tmp_page_num - num_of_cat / config.CMS_CFG['list_num'])
                    < 0.1 else tmp_page_num + 1)

        kwd = {
            'current_page': current_page_num,
            'count': num_of_cat,
            'pager_num': page_num,
            'config_num': config.CMS_CFG['list_num'],
            'kind': kind,
            'router': router_post[kind],
            'post_type': check_type[kind]
        }

        res = MPost.query_by_username(self.userinfo.user_name, state, kind, current_page_num)

        self.render('static_pages/check/publish_list.html',
                    userinfo=self.userinfo,
                    recs=res,
                    kwd=kwd,
                    state=state,
                    )
