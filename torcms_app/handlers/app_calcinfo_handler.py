# -*- coding:utf-8 -*-

'''
对App中计算的数值进行处理
'''
import json

from torcms.core.base_handler import BaseHandler
from torcms.core.tools import logger
from torcms.model.post_model import MPost
from torcms_app.model.ext_model import MCalcInfo


class CalcInfo(BaseHandler):
    def initialize(self):
        super(CalcInfo, self).initialize()
        self.minfo = MCalcInfo()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)
        data = MPost.get_by_uid(url_arr[0])
        json.dump(data.extinfo, self)

    def post(self, url_str=''):
        url_arr = self.parse_url(url_str)
        post_data = self.get_request_arguments()

        to_save_dic = {
            'infoid': url_arr[0],
            'userid': self.userinfo.uid,
            'extinfo': post_data,
        }

        logger.info('App Info: {0}'.format(url_arr[0]))
        logger.info('App UserID: {0}'.format(self.userinfo.uid))

        self.minfo.create_info(to_save_dic)

        # recs = self.minfo.query_all()
        # for x in recs:
        #     print(x.uid, x.extinfo)
