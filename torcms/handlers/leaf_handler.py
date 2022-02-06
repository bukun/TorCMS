# -*- coding:utf-8 -*-
'''
access via: /leaf/
            vs: /post/
The basic leaf handler.
The list of the posts should be ordered under leaf list.
'''

import tornado.escape
import tornado.ioloop
import tornado.web

from torcms.core import privilege
from torcms.core.tools import logger
from torcms.model.post_model import MPost

from .post_handler import PostHandler


class LeafHandler(PostHandler):
    '''
    The basic HTML Page handler.
    '''

    def initialize(self, **kwargs):
        super().initialize()
        self.kind = kwargs['kind'] if 'kind' in kwargs else '6'
        self.filter_view = kwargs[
            'filter_view'] if 'filter_view' in kwargs else False

    def post(self, *args, **kwargs):

        url_str = args[0]
        logger.info('Post url: {0}'.format(url_str))
        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['_edit']:
            self.update(url_arr[1])
        elif url_arr[0] in ['_add']:
            if len(url_arr) == 2:
                self.add(uid=url_arr[1])
            else:
                self.add()
        elif url_arr[0] == '_edit_kind':
            self._change_kind(url_arr[1])
        elif url_arr[0] in ['_cat_add']:
            self.add(catid=url_arr[1])
        elif url_arr[0] == 'update_order':
            self.update_order(url_arr[1], url_arr[2])
        elif len(url_arr) == 1 and len(url_str) == 5:
            self.add(uid=url_str)
        elif url_arr[0] == 'rel' and len(url_arr) == 3:
            self._add_relation(url_arr[1], url_arr[2])
        else:
            self.show404()

    @tornado.web.authenticated
    @privilege.auth_edit
    def update_order(self, uid, order):
        '''
        update the order of the posts.
        '''
        MPost.update_order(uid, order)
