# -*- coding:utf-8 -*-

from torcms.model.info_model import MInfor
from torcms.core.base_handler import BaseHandler
from torcms.model.info_relation_model import MRelInfor2Post
from torcms.model.info_relation_model import MRelPost2Infor
from torcms.model.post_model import MPost


class RelHandler(BaseHandler):
    def initialize(self):
        super(RelHandler, self).initialize()
        self.minfo = MInfor()
        self.mpost = MPost()
        self.rel_post2app = MRelPost2Infor()
        self.rel_app2post = MRelInfor2Post()

    def get(self, url_str=''):
        if len(url_str) > 0:
            ip_arr = url_str.split('/')
        else:
            return False
        if len(ip_arr) == 2:
            self.add_relation(ip_arr)

    def check_app(self, tt, uid):

        if tt == 'post':
            if False == self.mpost.get_by_id(uid):
                return False
        if tt == 'app':
            if False == self.minfo.get_by_uid(uid):
                return False
        return True

    def add_relation(self, url_arr):
        if self.check_app(url_arr[0], url_arr[1]):
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
                self.rel_post2app.add_relation(last_post_id, url_arr[1], 2)
                self.rel_app2post.add_relation(url_arr[1], last_post_id, 1)

        if url_arr[0] == 'post':
            if last_app_id:
                self.rel_app2post.add_relation(last_app_id, url_arr[1], 2)
                self.rel_post2app.add_relation(url_arr[1], last_app_id, 1)
