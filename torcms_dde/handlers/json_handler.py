# -*- coding:utf-8 -*-

'''
导出数据
'''
import json

from torcms.core.base_handler import BaseHandler

file_json = './torcms_dde/coor.json'


class JsonHandler(BaseHandler):
    def initialize(self):
        super(JsonHandler, self).initialize()

    def get(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", '*')
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1:
            if url_arr[0] == 'cruise-svr':
                self.cruise()
        else:
            self.show404()

    def cruise(self):
        file_gson = open(file_json, 'r', encoding='UTF-8')
        res = json.load(file_gson)
        for x in res:
            if 'url' in x:
                del x['url']
        out_dict = {
            'metainfo': {'desc': '网站服务所在地点。'},
            'results': res,
        }
        return json.dump(out_dict, self, ensure_ascii=False)
