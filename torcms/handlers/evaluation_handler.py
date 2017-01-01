# -*- coding:utf-8 -*-

import json
import tornado.web
from torcms.model.info_model import MInfor
from torcms.model.evaluation_model import MEvaluation
from torcms.model.usage_model import MUsage
from torcms.core.base_handler import BaseHandler
from torcms.model.info_relation_model import MInforRel


class EvaluationHandler(BaseHandler):
    def initialize(self):
        super(EvaluationHandler, self).initialize()
        self.mequa = MInfor()
        self.musage = MUsage()
        self.mrel = MInforRel()
        self.mcollect = MEvaluation()


    def get(self, url_str=''):

        url_arr = self.parse_url(url_str)
        if len(url_arr) == 0:
            return False

        # Just like  /evalucate/0123/1
        if len(url_arr) == 2 and len(url_arr[0]) == 4 and ( url_arr[1] in ['0', '1']):
            if self.get_current_user():
                self.add_or_update(url_arr[0], url_arr[1])
            else:
                self.set_status('403')
                return False
        return None



    @tornado.web.authenticated
    def add_or_update(self, app_id, value):
        self.mcollect.add_or_update(self.userinfo.uid, app_id, value)

        out_dic = {
            'eval0': self.mcollect.app_evaluation_count(app_id, 0),
            'eval1': self.mcollect.app_evaluation_count(app_id, 1)
        }

        return json.dump(out_dic, self)
