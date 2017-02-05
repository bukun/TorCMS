# -*- coding:utf-8 -*-

'''
For User collection
'''
import tornado.web
import json

from torcms.core.base_handler import BaseHandler
from torcms.model.collect_model import MCollect
from torcms.core.tools import logger


class CollectHandler(BaseHandler):
    def initialize(self):
        super(CollectHandler, self).initialize()

    def get(self, *args):
        url_str = args[0]
        if len(url_str) > 0:
            url_arr = self.parse_url(url_str)
        else:
            return False

        if url_str == 'list':
            self.list()
        elif len(url_arr) == 1 and (len(url_str) == 4 or len(url_str) == 5):
            if self.get_current_user():
                self.add_or_update(url_str)
            else:
                self.set_status(403)
                return False

    @tornado.web.authenticated
    def add_or_update(self, app_id):
        logger.info('Collect info: user-{0}, uid-{1}'.format(self.userinfo.uid, app_id))
        MCollect.add_or_update(self.userinfo.uid, app_id)
        out_dic = {'success': True}
        return json.dump(out_dic, self)

    @tornado.web.authenticated
    def list(self):
        self.render('user/collect/list.html',
                    recs_collect=MCollect.query_recent(self.userinfo.uid, 20),
                    userinfo=self.userinfo,
                    )
