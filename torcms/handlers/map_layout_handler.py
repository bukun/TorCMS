# coding:utf-8

import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.model.info_model import MInfor as MApp
from torcms.model.layout_model import MLayout


class MapLayoutHandler(BaseHandler):
    def initialize(self):
        super(MapLayoutHandler, self).initialize()
        self.mequa = MApp()
        self.mlayout = MLayout()

    def get(self, url_str):
        url_arr = self.parse_url(url_str)
        if len(url_arr) == 2:
            if url_arr[0] == 'delete':
                self.delete(url_arr[1])
        else:
            return False

    def post(self, url_str=''):
        if url_str == 'save':
            self.save_layout()
        else:
            return False

    @tornado.web.authenticated
    def delete(self, uid):
        self.mlayout.delete_by_uid(uid)

    @tornado.web.authenticated
    def save_layout(self):
        post_data = self.get_post_data()
        if 'zoom' in post_data:
            pass
        else:
            self.set_status(403)
            return
        post_data['user'] = self.userinfo.uid
        self.mlayout.add_or_update(post_data)
