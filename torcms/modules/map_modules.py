# -*- coding:utf-8 -*-

import tornado.web

from torcms.model.json_model import MJson
from torcms.model.layout_model import MLayout
from config import SITE_CFG


class MapJson(tornado.web.UIModule):
    def render(self, app_id, user_id):
        mjson = MJson()

        json_recs = mjson.query_by_app(app_id, user_id)

        kwd = {
            'pager': '',
            'signature': app_id,
            'tdesc': '',
            'site_url': SITE_CFG['site_url'],

        }

        return self.render_string('modules/map/map_json.html',
                                  json_recs=json_recs,
                                  app_id=app_id,
                                  kwd=kwd)


class MapLayout(tornado.web.UIModule):
    def render(self, app_id, user_id):
        mlayout = MLayout()

        layout_recs = mlayout.query_by_app(app_id, user_id)

        kwd = {
            'pager': '',
            'tdesc': '',
            'site_url': SITE_CFG['site_url'],

        }

        return self.render_string('modules/map/map_layout.html',
                                  layout_recs=layout_recs,
                                  kwd=kwd)
