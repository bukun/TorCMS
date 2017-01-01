# -*- coding:utf-8 -*-
import json

import tornado.web
import tornado.escape
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.model.json_model import MJson
from torcms.model.usage_model import MUsage


class GeoJsonHandler(BaseHandler):
    def initialize(self):
        super(GeoJsonHandler, self).initialize()
        self.mjson = MJson()
        self.musage = MUsage()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 0:
            self.index()

        elif url_str == 'draw':
            self.show_geojson('')

        elif url_arr[0] == 'list':
            self.list()
        elif len(url_arr) == 1 and len(url_str) == 4:
            self.show_geojson(url_str)

        elif len(url_arr) == 2:
            if url_arr[0] == 'gson':
                rec = self.mjson.get_by_id(url_arr[1])
                if rec:
                    return json.dump(rec.json, self)
                else:
                    return False

            elif url_arr[0] == 'download':
                self.download(url_arr[1])
            elif url_arr[0] == 'delete':
                self.delete(url_arr[1])

    def show_geojson(self, gid):
        kwd = {
            'pager': '',
            'url': self.request.uri,
            'geojson': gid,
            'tdesc': '',
            'login': 1 if self.get_current_user() else 0,

        }

        map_hist = []
        if self.get_secure_cookie('map_hist'):
            for xx in range(0, len(self.get_secure_cookie('map_hist').decode('utf-8')), 4):
                map_hist.append(self.get_secure_cookie('map_hist').decode('utf-8')[xx: xx + 4])
        self.render('infor/app/full_screen_draw.html',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    recent_apps=self.musage.query_recent(self.get_current_user(), 6)[1:] if self.userinfo else [],

                    )

    def index(self):
        self.render('infor/geojson/index.html',
                    kwd={},
                    userinfo=self.userinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    json_arr=self.mjson.query_recent(self.userinfo.uid, 20) if self.userinfo else [],

                    )

    @tornado.web.authenticated
    def list(self):

        kwd = {}
        self.render('infor/geojson/gson_recent.html',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    json_arr=self.mjson.query_recent(self.userinfo.uid, 10),
                    )

    @tornado.web.authenticated
    def delete(self, uid):
        self.mjson.delete_by_uid(uid)

    @tornado.web.authenticated
    def download(self, pa_str):
        uid = pa_str.split('_')[-1].split('.')[0]

        self.set_header('Content-Type', 'application/force-download')
        rec = self.mjson.get_by_id(uid)

        geojson = rec.json

        out_arr = []
        for key in geojson.keys():
            out_arr = out_arr + geojson[key]['features']

        out_dic = {"type": "FeatureCollection",
                   "features": out_arr}

        if rec:
            return json.dump(out_dic, self)

    def post(self, url_str=''):

        url_arr = self.parse_url(url_str)

        if len(url_arr) <= 1:
            self.add_data(url_str)
        elif len(url_arr) == 2:
            if self.get_current_user():
                self.add_data_with_map(url_arr)
            else:
                self.set_status('403')
                return False
        else:
            self.set_status('403')
            return False

    @tornado.web.authenticated
    def add_data(self, gson_uid):
        post_data = self.get_post_data()

        geojson_str = post_data['geojson']

        json_obj = json.loads(geojson_str)

        out_dic = {}
        index = 0

        for x in json_obj['features']:
            bcbc = x['geometry']
            if 'features' in bcbc:
                if bcbc['features'][0]['geometry']['coordinates'] in [[], [[None]]]:
                    continue
            else:
                if bcbc['coordinates'] in [[], [[None]]]:
                    continue

                bcbc = {'features': [{'geometry': bcbc,
                                      "properties": {},
                                      "type": "Feature"}],
                        'type': "FeatureCollection"}

            out_dic[index] = bcbc
            index = index + 1

        if gson_uid == 'draw' or gson_uid == '':
            uid = tools.get_uu4d()
            while self.mjson.get_by_id(uid):
                uid = tools.get_uu4d()
            return_dic = {'sig': uid}

        elif len(gson_uid) == 4:
            uid = gson_uid
            return_dic = {'sig': ''}

            cur_info = self.mjson.get_by_id(uid)

            if cur_info.user_id == self.userinfo.uid:
                pass
            else:
                return_dic['status'] = 0
                return json.dump(return_dic, self)
        else:
            return

        try:
            self.mjson.add_or_update_json(uid, self.userinfo.uid, out_dic)
            return_dic['status'] = 1
            return json.dump(return_dic, self)
        except:
            self.set_status(400)
            return False

    @tornado.web.authenticated
    def add_data_with_map(self, url_arr):

        post_data = self.get_post_data()
        geojson_str = post_data['geojson']
        json_obj = json.loads(geojson_str)

        out_dic = {}
        index = 0

        for x in json_obj['features']:
            bcbc = x['geometry']
            if 'features' in bcbc:
                if bcbc['features'][0]['geometry']['coordinates'] in [[], [[None]]]:
                    continue
            else:
                if bcbc['coordinates'] in [[], [[None]]]:
                    continue

                bcbc = {'features': [{'geometry': bcbc,
                                      "properties": {},
                                      "type": "Feature"}],
                        'type': "FeatureCollection"}

            out_dic[index] = bcbc
            index = index + 1

        if len(url_arr[1]) == 4:
            uid = url_arr[1]
            return_dic = {'sig': ''}

            cur_info = self.mjson.get_by_id(uid)

            if cur_info.user_id == self.userinfo.uid:
                pass
            else:
                return_dic['status'] = 0
                return json.dump(return_dic, self)
        else:
            uid = tools.get_uu4d()
            while self.mjson.get_by_id(uid):
                uid = tools.get_uu4d()
            return_dic = {'sig': uid}

        self.mjson.add_or_update(uid, self.userinfo.uid, url_arr[0], out_dic)
        return_dic['status'] = 1
        return json.dump(return_dic, self)
