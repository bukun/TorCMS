# -*- coding:utf-8 -*-

'''
Handlers for Map application.
'''

import tornado.escape
import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.model.post_model import MPost
from torcms_maplet.core.tools import average_array


class MapViewHandler(BaseHandler):
    '''
    For map overlay.
    '''

    def initialize(self):
        super(MapViewHandler, self).initialize()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if len(url_arr) > 1:
            if url_arr[0] == 'overlay':
                self.show_overlay(url_arr[1:])
            elif url_arr[0] == 'sync':
                self.show_sync(url_arr[1:])

            elif url_arr[0] == 'split':
                self.show_split(url_arr[1:])
        else:
            kwd = {'title': '', 'info': ''}
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

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
            c_ap = MPost.get_by_uid(app_rr)
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
            'zoom_current': int(average_array(zoom_current_zrr)),
        }
        if 'fullscreen' in self.request.arguments:
            tmpl = '../torcms_maplet/tmpl/mapview/overlay_full.html'
        else:
            tmpl = '../torcms_maplet/tmpl/mapview/overlay.html'
        self.render(
            tmpl,
            topmenu='',
            kwd=kwd,
            userinfo=self.userinfo,
            unescape=tornado.escape.xhtml_unescape,
            app_arr=app_info_arr,
            app_str='/'.join(app_arr),
        )

    def show_sync(self, app_arr):
        '''
        Sync view for two maps.
        '''
        app_info_arr = []
        lon_arr = []
        lat_arr = []
        zoom_max_arr = []
        zoom_min_arr = []
        zoom_current_zrr = []

        for app_rr in app_arr:
            c_ap = MPost.get_by_uid(app_rr)
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
            'zoom_current': int(average_array(zoom_current_zrr)),
        }

        tmpl = '../torcms_maplet/tmpl/mapview/sync_full.html'
        self.render(
            tmpl,
            topmenu='',
            kwd=kwd,
            userinfo=self.userinfo,
            unescape=tornado.escape.xhtml_unescape,
            app_arr=app_info_arr,
            app_str='/'.join(app_arr),
        )

    def show_split(self, app_arr):
        '''
        Splitting view for two maps.
        '''
        app_info_arr = []
        lon_arr = []
        lat_arr = []
        zoom_max_arr = []
        zoom_min_arr = []
        zoom_current_zrr = []

        for app_rr in app_arr:
            c_ap = MPost.get_by_uid(app_rr)
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
            'zoom_current': int(average_array(zoom_current_zrr)),
        }

        tmpl = '../torcms_maplet/tmpl/mapview/split_full.html'
        self.render(
            tmpl,
            topmenu='',
            kwd=kwd,
            userinfo=self.userinfo,
            unescape=tornado.escape.xhtml_unescape,
            app_arr=app_info_arr,
            app_str='/'.join(app_arr),
        )
