# -*- coding:utf-8 -*-


import json

import tornado.escape
import tornado.web

from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.model.usage_model import MUsage
from torcms_maplet.model.json_model import MJson


class GeoJsonHandler(BaseHandler):
    def initialize(self):
        super(GeoJsonHandler, self).initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_arr:
            self.index()
        elif url_str == 'draw':
            self.show_geojson('')
        elif url_arr[0] == 'list':
            self.list()
        elif len(url_arr) == 1 and len(url_str) == 4:
            self.show_geojson(url_str)
        elif len(url_arr) == 2:
            if url_arr[0] == 'gson':
                rec = MJson.get_by_id(url_arr[1])
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
            for the_index in range(
                0, len(self.get_secure_cookie('map_hist').decode('utf-8')), 4
            ):
                map_hist.append(
                    self.get_secure_cookie('map_hist').decode('utf-8')[
                        the_index : the_index + 4
                    ]
                )

        self.render(
            '../torcms_maplet/tmpl/full_screen_draw.html',
            kwd=kwd,
            userinfo=self.userinfo,
            unescape=tornado.escape.xhtml_unescape,
            recent_apps=(
                MUsage.query_recent(self.userinfo.uid, 'm', 6)[1:]
                if self.userinfo
                else []
            ),
        )

    def index(self):
        self.render(
            '../torcms_maplet/tmpl/geojson/gson_index.html',
            kwd={},
            userinfo=self.userinfo,
            unescape=tornado.escape.xhtml_unescape,
            json_arr=MJson.query_recent(self.userinfo.uid, 20) if self.userinfo else [],
        )

    @tornado.web.authenticated
    def list(self):
        kwd = {}
        self.render(
            '../torcms_maplet/tmpl/geojson/gson_recent.html',
            kwd=kwd,
            userinfo=self.userinfo,
            unescape=tornado.escape.xhtml_unescape,
            json_arr=MJson.query_recent(self.userinfo.uid, 10),
        )

    @tornado.web.authenticated
    def delete(self, uid):
        MJson.delete_by_uid(uid)

    def put(self, *args, **kwargs):
        print('Got `put`')

    @tornado.web.authenticated
    def download(self, pa_str):
        '''
        Download the GeoJson to file.
        :param pa_str:
        :return:
        '''
        uid = pa_str.split('_')[-1].split('.')[0]
        self.set_header('Content-Type', 'application/force-download')
        rec = MJson.get_by_id(uid)
        geojson = rec.json
        out_arr = []
        for key in geojson.keys():
            out_arr = out_arr + geojson[key]['features']

        out_dic = {"type": "FeatureCollection", "features": out_arr}

        if rec:
            return json.dump(out_dic, self)

    def post(self, *args, **kwargs):
        print('Got `post`')
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        if len(url_arr) <= 1:
            self.add_data(url_str)
        elif len(url_arr) == 2:
            if self.get_current_user():
                self.add_data_with_map(url_arr)
            else:
                self.set_status(403)
                return False
        else:
            self.set_status(403)
            return False

    def parse_geojson(self, geojson_str):
        '''
        Parse the GeoJson from string.
        :param geojson_str:
        :return:
        '''

        def get_geometry(geom):
            '''
            Get geometry from GeoJson.
            :param geom:
            :return:
            '''
            bcbc = geom['geometry']
            if 'features' in bcbc:
                if bcbc['features'][0]['geometry']['coordinates'] in [[], [[None]]]:
                    return
            else:
                if bcbc['coordinates'] in [[], [[None]]]:
                    return

                bcbc = {
                    'features': [
                        {'geometry': bcbc, "properties": {}, "type": "Feature"}
                    ],
                    'type': "Feature",
                }
            return bcbc

        json_obj = json.loads(geojson_str)
        out_dic = {}
        index = 0

        for the_fea in json_obj['features']:
            if the_fea['type'] == 'Feature':
                out_dic[index] = get_geometry(the_fea)
                index += 1
            elif the_fea['type'] == 'FeatureCollection':
                for fea_in_fea in the_fea['features']:
                    out_dic[index] = get_geometry(fea_in_fea)
                    index += 1
        return out_dic

    @tornado.web.authenticated
    def add_data(self, gson_uid):
        '''
        Post via adding.
        '''
        post_data = self.get_request_arguments()
        geojson_str = post_data['geojson']
        out_dic = self.parse_geojson(geojson_str)

        if gson_uid == 'draw' or gson_uid == '':
            uid = tools.get_uu4d()
            while MJson.get_by_id(uid):
                uid = tools.get_uu4d()
            return_dic = {'uid': uid}
        elif len(gson_uid) == 4:
            uid = gson_uid
            return_dic = {'uid': ''}
            cur_info = MJson.get_by_id(uid)
            if cur_info.user_id == self.userinfo.uid:
                pass
            else:
                return_dic['status'] = 0
                return json.dump(return_dic, self)
        else:
            return

        try:
            MJson.add_or_update_json(
                uid, self.userinfo.uid, out_dic, post_data, version=1
            )
            return_dic['status'] = 1
        except Exception:
            self.set_status(400)
            return_dic['status'] = 0
        return json.dump(return_dic, self)

    @tornado.web.authenticated
    def add_data_with_map(self, url_arr):
        post_data = self.get_request_arguments()
        geojson_str = post_data['geojson']
        out_dic = self.parse_geojson(geojson_str)

        if len(url_arr[1]) == 4:
            uid = url_arr[1]
            return_dic = {'sig': ''}
            cur_info = MJson.get_by_id(uid)
            if cur_info.user_id == self.userinfo.uid:
                pass
            else:
                return_dic['status'] = 0
                return json.dump(return_dic, self)
        else:
            uid = tools.get_uu4d()
            while MJson.get_by_id(uid):
                uid = tools.get_uu4d()
            return_dic = {'sig': uid}

        MJson.add_or_update(uid, self.userinfo.uid, url_arr[0], out_dic)
        return_dic['status'] = 1
        return json.dump(return_dic, self)


class GeoJsonAjaxHandler(GeoJsonHandler):
    def initialize(self, **kwargs):
        print('init...')
        super(GeoJsonAjaxHandler, self).initialize()
        self.set_default_headers()

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self, *args, **kwargs):
        print('Get')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        print(args)
        uid = args[0]
        gson = MJson.get_by_uid(uid)

        if gson:
            out_dic = {
                'uid': uid,
                'geojson': gson.json,
            }
        else:
            out_dic = {'uid': 0}
        return json.dump(out_dic, self)

    def put(self, *args, **kwargs):
        print('Put')

    def post(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

        url_arr = self.parse_url(args[0])
        print(url_arr)
        if len(url_arr) > 0:
            if url_arr[0] == '_add':
                self.j_add()
            elif url_arr[0] == '_edit':
                self.j_add(url_arr[1])

    def j_add(self, uid=''):
        post_data = self.get_request_arguments()
        print(post_data)
        geojson_str = post_data['geojson']
        # out_dic = self.parse_geojson(geojson_str)

        if uid:
            pass
        else:
            uid = 'x' + tools.get_uu4d()[1:]
            while MJson.get_by_id(uid):
                uid = 'x' + tools.get_uu4d()[1:]
        return_dic = {'uid': uid}

        # MJson.add_or_update_json(uid, self.userinfo.uid, out_dic)
        # return_dic['status'] = 1
        # return json.dump(return_dic, self)

        try:
            MJson.add_or_update_json(uid, '', geojson_str, post_data)
            return_dic['status'] = 1
            return json.dump(return_dic, self)
        except Exception:
            self.set_status(400)
            return_dic['status'] = 0
            return json.dump(return_dic, self)
