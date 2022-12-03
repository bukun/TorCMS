# -*- coding:utf-8 -*-

'''
地图日志
'''

from torcms.core.base_handler import BaseHandler
from torcms_maplet.model.map_log_model import MMapLog


class MapLogHandler(BaseHandler):
    def initialize(self, **kwargs):
        super(MapLogHandler, self).initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]

        if url_str == '':
            self.list()
        else:
            self.show404()

    def post(self, *args, **kwargs):

        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_arr[0] == '_add':
            self.add()
        else:
            self.show404()

    def add(self):
        '''
        添加地图日志
        '''

        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)[0]
        if self.userinfo:
            post_data['user'] = self.userinfo.uid
        else:
            post_data['user'] = ''
        post_data['user_ip'] = self.get_host_ip()

        MMapLog.add(post_data)

        return True

    def list(self):
        '''
         地图日志列表
        '''
        kwd = {}
        recs = MMapLog.get_all()
        self.render('../torcms_maplet/map_log.html',
                    recs=recs,
                    kwd=kwd,
                    userinfo=self.userinfo)
