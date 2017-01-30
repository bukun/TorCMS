# -*- coding:utf-8 -*-

'''
Handlers for Map application.
'''

import tornado.escape
import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.core.tools import average_array
from torcms.model.info_model import MInfor
from torcms.model.layout_model import MLayout
from torcms.handlers.info_handler import InfoHandler


class MapPostHandler(InfoHandler):
    '''
    For meta handler of map.
    '''

    def initialize(self, **kwargs):
        super(MapPostHandler, self).initialize()
        self.kind = 'm'

    def ext_view_kwd(self, info_rec):
        post_data = self.get_post_data()

        out_dic = {
            'marker': 1 if 'marker' in post_data else 0,
            'geojson': post_data['gson'] if 'gson' in post_data else '',
            'map_hist_arr': self.extra_view(info_rec.uid),

        }
        if 'zoom' in post_data:
            out_dic['vzoom'] = post_data['zoom']
        if 'lat' in post_data:
            out_dic['vlat'] = post_data['lat']
        if 'lon' in post_data:
            out_dic['vlon'] = post_data['lon']

        return out_dic

    def extra_view(self, app_id):
        qian = self.get_secure_cookie('map_hist')
        if qian:
            qian = qian.decode('utf-8')
        else:
            qian = ''
        self.set_secure_cookie('map_hist', (app_id + qian)[:20])
        map_hist = []
        if self.get_secure_cookie('map_hist'):
            for idx in range(0, len(self.get_secure_cookie('map_hist').decode('utf-8')), 4):
                map_hist.append(self.get_secure_cookie('map_hist').decode('utf-8')[idx: idx + 4])
        return map_hist

    def ext_tmpl_name(self, rec):
        if 'fullscreen' in self.request.arguments:
            tmpl = 'post_{0}/full_screen.html'.format(self.kind)
        else:
            tmpl = 'post_{0}/show_map.html'.format(self.kind)
        return tmpl


class MapAdminHandler(MapPostHandler):
    '''
    Extra defined the class, for it could be added into InfoHandler.
    '''

    def post(self, *args):
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        if url_arr[0] == '_update_view':
            self.update_view(url_arr[1])

    def update_view(self, uid):
        post_data = self.get_post_data()

        zoom_current = int(post_data['ext_zoom_current'])
        if zoom_current == 0:
            return False
        post_data['ext_zoom_max'] = str(zoom_current + 3)
        post_data['ext_zoom_min'] = str(zoom_current - 1)

        self.minfor.update_jsonb(uid, post_data)


class MapLayoutHandler(BaseHandler):
    '''
    Layerout for map handler.
    '''

    def initialize(self):
        super(MapLayoutHandler, self).initialize()
        self.mequa = MInfor()
        self.mlayout = MLayout()

    def get(self, *args):
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        if len(url_arr) == 2:
            if url_arr[0] == 'delete':
                self.delete(url_arr[1])
        else:
            return False

    def post(self, *args):
        url_str = args[0]
        if url_str == 'save':
            self.save_layout()
        else:
            return False

    @tornado.web.authenticated
    def delete(self, uid):
        '''
        Delete the map layout of user.
        :param uid:
        :return:
        '''
        self.mlayout.delete_by_uid(uid)

    @tornado.web.authenticated
    def save_layout(self):
        '''
        Save the map layout.
        :return:
        '''
        post_data = self.get_post_data()
        if 'zoom' in post_data:
            pass
        else:
            self.set_status(403)
            return
        post_data['user'] = self.userinfo.uid
        self.mlayout.add_or_update(post_data)


class MapOverlayHandler(BaseHandler):
    '''
    For map overlay.
    '''

    def initialize(self):
        super(MapOverlayHandler, self).initialize()
        self.mapplication = MInfor()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if len(url_arr) > 1:
            self.show_overlay(url_arr)
        else:
            kwd = {
                'title': '',
                'info': '',
            }
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo)

    def show_overlay(self, app_arr):
        '''
        Open two maps on one screen.
        '''
        app_info_arr = []
        lon_arr = []
        lat_arr = []
        zoom_max_arr = []
        zoom_min_arr = []
        zoom_current_zrr = []

        for app_rr in app_arr:
            c_ap = self.mapplication.get_by_uid(app_rr)
            app_info_arr.append(c_ap)
            lon_arr.append(float(c_ap.extinfo['ext_lon']))
            lat_arr.append(float(c_ap.extinfo['ext_lat']))
            zoom_max_arr.append(int(c_ap.extinfo['ext_zoom_max']))
            zoom_min_arr.append(int(c_ap.extinfo['ext_zoom_min']))
            zoom_current_zrr.append(int(c_ap.extinfo['ext_zoom_current']))

        kwd = {
            'url': 1,
            'cookie_str': '',
            'lon': average_array(lon_arr),
            'lat': average_array(lat_arr),
            'zoom_max': max(zoom_max_arr),
            'zoom_min': min(zoom_min_arr),
            'zoom_current': int(average_array(zoom_current_zrr))
        }
        if 'fullscreen' in self.request.arguments:
            tmpl = 'post_m/overlay/overlay_full.html'
        else:
            tmpl = 'post_m/overlay/overlay.html'
        self.render(
            tmpl,
            topmenu='',
            kwd=kwd,
            userinfo=self.userinfo,
            unescape=tornado.escape.xhtml_unescape,
            app_arr=app_info_arr,
            app_str='/'.join(app_arr)
        )
