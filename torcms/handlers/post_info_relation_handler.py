# -*- coding:utf-8 -*-

# from torcms.model.info_model import MInfor
from torcms.core.base_handler import BaseHandler
from torcms.model.relation_model import MRelation
from torcms.model.post_model import MPost


class RelHandler(BaseHandler):
    def initialize(self):
        super(RelHandler, self).initialize()

    def get(self, url_str=''):
        if len(url_str) > 0:
            ip_arr = url_str.split('/')
        else:
            return False
        if len(ip_arr) == 2:
            self.add_relation(ip_arr)

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
