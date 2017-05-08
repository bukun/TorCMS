# -*- coding:utf-8 -*-

'''
Relationship between Posts.
'''

from torcms.core.base_handler import BaseHandler
from torcms.model.relation_model import MRelation
from torcms.model.post_model import MPost


class RelHandler(BaseHandler):
    def initialize(self):
        super(RelHandler, self).initialize()

    def get(self, *args):
        url_str = args[0]

        url_arr = self.parse_url(url_str)

        if len(url_arr) == 2:
            self.add_relation(url_arr)
        else:
            return False

    def add_relation(self, url_arr):
        '''
        Add relationship.
        :param url_arr:
        :return:
        '''
        if MPost.get_by_uid(url_arr[1]):
            pass
        else:
            return False

        last_post_id = self.get_secure_cookie('last_post_uid')
        if last_post_id:
            last_post_id = last_post_id.decode('utf-8')

        last_app_id = self.get_secure_cookie('use_app_uid')
        if last_app_id:
            last_app_id = last_app_id.decode('utf-8')

        if url_arr[0] == 'info':
            if last_post_id:
                MRelation.add_relation(last_post_id, url_arr[1], 2)
                MRelation.add_relation(url_arr[1], last_post_id, 1)

        if url_arr[0] == 'post':
            if last_app_id:
                MRelation.add_relation(last_app_id, url_arr[1], 2)
                MRelation.add_relation(url_arr[1], last_app_id, 1)
