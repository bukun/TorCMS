# -*- coding:utf-8 -*-

'''
Define the map module for TorCMS.
'''

import tornado.web

from config import SITE_CFG
from torcms.model.post_model import MPost
from torcms_maplet.model.json_model import MJson
from torcms_maplet.model.layout_model import MLayout


class MapAd(tornado.web.UIModule):
    def render(self, num=10, with_catalog=True, with_date=True):
        mrecs = MPost.query_random(num=1, kind='m')
        if mrecs.count() > 0:
            mrec = mrecs.get()
            return self.render_string(
                '../torcms_maplet/tmpl_modules/map_ad.html',
                mapinfo=mrec,
            )
        else:
            return ''


class MapJson(tornado.web.UIModule):
    '''
    List the jsons records for centain Map.
    '''

    def render(self, *args, **kwargs):
        app_id = args[0]
        user_id = args[1]

        # mjson = MJson()

        json_recs = MJson.query_by_app(app_id, user_id)

        print('x-x-x' * 10)
        print(json_recs.count())

        kwd = {
            'pager': '',
            'signature': app_id,
            'tdesc': '',
            'site_url': SITE_CFG['site_url'],
        }

        return self.render_string(
            '../torcms_maplet/tmpl_modules/map_json.html',
            json_recs=json_recs,
            app_id=app_id,
            kwd=kwd,
        )


class MapLayout(tornado.web.UIModule):
    '''
    List the Layout of Map.
    '''

    def render(self, *args, **kwargs):
        app_id = args[0]
        user_id = args[1]
        mlayout = MLayout()
        layout_recs = mlayout.query_by_app(app_id, user_id)

        kwd = {'pager': '', 'tdesc': '', 'site_url': SITE_CFG['site_url']}

        return self.render_string(
            '../torcms_maplet/tmpl_modules/map_layout.html',
            layout_recs=layout_recs,
            kwd=kwd,
        )
