# -*- coding:utf-8 -*-

'''
For the evaluation of the posts.
'''
import json
import tornado.web
from torcms.model.evaluation_model import MEvaluation
from torcms.core.base_handler import BaseHandler


class EvaluationHandler(BaseHandler):
    '''
    For the evaluation of the posts.
    '''

    def initialize(self, **kwargs):
        super(EvaluationHandler, self).initialize()

    def get(self, *args, **kwargs):
        url_arr = self.parse_url(args[0])

        # Just like  /evalucate/0123/1
        if len(url_arr) == 2 and len(url_arr[0]) == 4 and (url_arr[1] in ['0', '1']):
            if self.get_current_user():
                self.add_or_update(url_arr[0], url_arr[1])
            else:
                self.set_status(403)
                return None
        else:
            return None

    @tornado.web.authenticated
    def add_or_update(self, app_id, value):
        '''
        Adding or updating the evalution.
        :param app_id:  the ID of the post.
        :param value: the evaluation
        :return:  in JSON format.
        '''
        MEvaluation.add_or_update(self.userinfo.uid, app_id, value)

        out_dic = {
            'eval0': MEvaluation.app_evaluation_count(app_id, 0),
            'eval1': MEvaluation.app_evaluation_count(app_id, 1)
        }

        return json.dump(out_dic, self)
