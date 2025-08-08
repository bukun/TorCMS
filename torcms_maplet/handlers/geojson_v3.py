# -*- coding:utf-8 -*-
import json

import tornado.escape
import tornado.web

from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.model.usage_model import MUsage
from torcms_maplet.core.webdog_to_geojson import webdog_to_geojson
from torcms_maplet.model.json_model import MJson


class GeoJsonHandler(BaseHandler):
    def initialize(self):
        super(GeoJsonHandler, self).initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 0:
            self.index()
        elif url_str == 'draw':
            self.show_geojson('')
        elif url_arr[0] == 'list':
            self.list()
        elif url_arr[0] == '_delete':
            self.delete(url_arr[1])
        elif url_arr[0] == '_edit':
            self.edit(url_arr[1])
        elif len(url_arr) == 1 and len(url_str) == 4:
            self.show_geojson(url_str)
        elif len(url_arr) == 2:
            if url_arr[0] == 'gson':
                rec = MJson.get_by_id(url_arr[1])
                # print('i' * 40)
                # print(rec.json)

                if 'tileLayer' in rec.json:
                    # if the data is webdog.
                    uu = rec.json
                    # print('=x' * 20)
                    for key in uu.keys():
                        val = uu[key]
                        print(key)
                        if type(val) == type({}):
                            for key2 in val.keys():
                                print(' ' * 4 + key2)

                                val2 = val[key2]
                                if type(val2) == type({}):
                                    for key3 in val2.keys():
                                        print(' ' * 8 + key3 + ':' + str(val2[key3]))

                    # print('-=' * 20)
                    geoinfo = json.loads(webdog_to_geojson(uu))
                    # print(geoinfo)

                else:
                    # if the old geojson data.
                    geoinfo = {'features': rec.json}
                if rec:
                    return json.dump(geoinfo['features'], self)
                else:
                    return False

            elif url_arr[0] == 'download':
                self.download(url_arr[1])
            elif url_arr[0] == 'delete':
                self.delete(url_arr[1])

    def post(self, *args, **kwargs):
        url_arr = self.parse_url(args[0])

        if len(url_arr) == 1:
            self.add_data(url_arr[0])
        elif len(url_arr) == 2:
            if url_arr[0] == '_edit':
                self.update_meta(url_arr[1])
            elif self.get_current_user():
                self.add_data_with_map(url_arr)
            else:
                self.set_status(403)
                return False
        else:
            self.set_status(403)
            return False

    def show_geojson(self, gid):
        gsoninfo = MJson.get_by_uid(gid)
        kwd = {
            'pager': '',
            'url': self.request.uri,
            'geojson': gid,
            'tdesc': '',
            'login': 1 if self.get_current_user() else 0,
        }

        map_hist = []
        if self.get_secure_cookie('map_hist'):
            for xx in range(
                0, len(self.get_secure_cookie('map_hist').decode('utf-8')), 4
            ):
                map_hist.append(
                    self.get_secure_cookie('map_hist').decode('utf-8')[xx : xx + 4]
                )

        self.render(
            # '../torcms_maplet/tmpl/full_screen_draw.html',
            '../torcms_maplet/tmpl/full_screen_draw_v2.html',
            kwd=kwd,
            userinfo=self.userinfo,
            unescape=tornado.escape.xhtml_unescape,
            gsoninfo=gsoninfo,
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
            json_arr=MJson.query_recent(num=20),
        )

    @tornado.web.authenticated
    def edit(self, uid):
        postinfo = MJson.get_by_uid(uid)
        if postinfo:
            pass
        else:
            return self.show404()

        self.render(
            '../torcms_maplet/tmpl/geojson/gson_edit.html',
            postinfo=postinfo,
            userinfo=self.userinfo,
        )

    @tornado.web.authenticated
    def delete(self, uid):
        MJson.delete_by_uid(uid)
        self.redirect('/geojson/')

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

    def update_meta(self, gson_uid):
        post_data = self.get_request_arguments()
        out_dic = post_data['geojson']
        uid = gson_uid
        return_dic = {'uid': ''}
        cur_info = MJson.get_by_id(uid)
        if cur_info.user_id == self.userinfo.uid:
            pass
        else:
            return False

        MJson.add_or_update_json(uid, self.userinfo.uid, out_dic, post_data)
        self.redirect('/geojson/')

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

        for x in json_obj['features']:
            if x['type'] == 'Feature':
                out_dic[index] = get_geometry(x)
                index += 1
            elif x['type'] == 'FeatureCollection':
                for y in x['features']:
                    out_dic[index] = get_geometry(y)
                    index += 1

        return out_dic

    @tornado.web.authenticated
    def add_data(self, gson_uid):
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
                uid, self.userinfo.uid, out_dic, post_data, version=3
            )
            return_dic['status'] = 1
        except Exception:
            self.set_status(400)
            return_dic['status'] = 0
        return json.dump(return_dic, self)

    @tornado.web.authenticated
    def add_data_with_map(self, url_arr):
        '''
        Add geojson from Map
        :param url_arr:
        :return:
        '''

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
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        # print(args)
        url_arr = self.parse_url(args[0])

        if url_arr[0] == '_draw':
            uid = url_arr[1]
            gson = MJson.get_by_uid(uid)
            if gson:
                out_dic = {
                    'uid': uid,
                    # 'geojson': gson.json,
                    'geojson': json.dumps(gson.json),
                }
            else:
                out_dic = {'uid': 0}
        else:
            out_dic = {'uid': 0}
        print('From GeoJson Ajax get ...')
        print(out_dic)
        return json.dump(out_dic, self)

    def put(self, *args, **kwargs):
        print('Put')

    def post(self, *args, **kwargs):
        print('Post')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        url_arr = self.parse_url(args[0])
        print(url_arr)

        if len(url_arr) > 0:
            if url_arr[0] in ['_draw', '_add']:
                self.j_add()
                if len(url_arr) > 1:
                    self.j_add(url_arr[1])
            else:
                return False

    def j_add(self, uid=''):
        if self.userinfo:
            pass
        else:
            print('User Not Login.')
        print('=' * 20)
        print('Hello')
        post_data = self.get_request_arguments()

        # print(post_data)

        geojson_str = post_data['geojson']
        gson = json.loads(geojson_str)
        print(json.dumps(gson, indent=1))

        # maplet_map_id = 'm' + gson['tileLayer']['high']['name'].split('-')[-1]
        maplet_map_id = 'mv000'
        if uid:
            pass
        else:
            uid = tools.get_uu4d()
            while MJson.get_by_id(uid):
                uid = tools.get_uu4d()
        return_dic = {'uid': uid}

        # MJson.add_or_update(uid, 'xxxx', maplet_map_id, gson)

        try:
            # MJson.add_or_update_json(uid, '', geojson_str)
            # print(self.userinfo.uid, )
            # print(maplet_map_id),
            # print(geojson_str)
            MJson.add_or_update(uid, 'xxxx', maplet_map_id, gson, version=3)
            return_dic['status'] = 1
            # print('Saved successfully!')
            return json.dump(return_dic, self)

        except Exception:
            self.set_status(400)
            return_dic['status'] = 0
            # print('Save Error!')
            return json.dump(return_dic, self)
