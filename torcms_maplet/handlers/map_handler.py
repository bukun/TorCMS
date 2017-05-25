# -*- coding:utf-8 -*-

'''
Handlers for Map application.
'''

import tornado.escape
import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.core.tools import average_array
from torcms.handlers.post_handler import PostHandler
from torcms.model.post_model import MPost
from torcms_maplet.model.layout_model import MLayout


class MapPostHandler(PostHandler):
    '''
    For meta handler of map.
    '''

    def initialize(self, **kwargs):
        super(MapPostHandler, self).initialize()
        self.kind = 'm'

    def _redirect(self, url_arr):
        '''
        Redirection.
        :param url_arr:
        :return:
        '''
        direct_dic = {
            'recent': '/post_list/recent',
            'refresh': '/post_list/_refresh',
            '_refresh': '/post_list/_refresh',

        }
        sig = url_arr[0]
        for sig_enum in direct_dic:
            if sig == sig_enum:
                self.redirect(direct_dic[sig])
        pre_dic = {
            'cat_add': '_cat_add',
            'add_document': '_add',
            'add': '_add',
            'modify': '_edit',
            'edit': '_edit',
            'delete': '_delete',
            'ajax_count_plus': 'j_count_plus',
        }
        sig = url_arr[0]
        for sig_enum in pre_dic:
            if sig == sig_enum:
                url_arr = [pre_dic[sig_enum]] + url_arr[1:]
                url_str = '/post/' + '/'.join(url_arr)
                self.redirect(url_str)
        return True

    def get(self, *args):

        url_str = args[0]
        url_arr = self.parse_url(url_str)
        if len(url_arr) > 0:
            self._redirect(url_arr)

        if url_str == '':
            self.index()
        elif url_arr[0] == '_cat_add':
            self._to_add(catid=url_arr[1])
        elif url_arr[0] == '_add':
            if len(url_arr) == 2:
                self._to_add(uid=url_arr[1])
            else:
                self._to_add()
        elif url_arr[0] == '_edit_kind':
            self._to_edit_kind(url_arr[1])
        elif url_arr[0] == '_edit':
            self._to_edit(url_arr[1])
        elif url_arr[0] == '_delete':
            self.delete(url_arr[1])
        elif url_arr[0] == 'j_delete':
            self.j_delete(url_arr[1])
        elif url_arr[0] == 'j_count_plus':
            self.j_count_plus(url_arr[1])
        elif len(url_arr) == 1 and url_str.endswith('.html'):
            # Deprecated
            self.redirect('/post/{uid}'.format(uid=url_str.split('.')[0]))
        elif len(url_arr) == 1 and len(url_str) in [4]:
            self.redirect('/map/m' + url_str)
        elif len(url_arr) == 1 and len(url_str) in [5]:
            self.view_or_add(url_str)
        else:
            kwd = {
                'title': '',
                'info': '404. Page not found!',
            }
            self.set_status(404)
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )

    # @tornado.web.authenticated
    # def __to_edit(self, infoid):
    #     '''
    #     render the HTML page for post editing.
    #     :param infoid:
    #     :return:
    #     '''
    #     if self.check_post_role()['EDIT']:
    #         pass
    #     else:
    #         return False
    #
    #     rec_info = MPost.get_by_uid(infoid)
    #     postinfo = rec_info
    #
    #     if rec_info:
    #         pass
    #     else:
    #         self.render('html/404.html')
    #         return
    #
    #     if 'def_cat_uid' in rec_info.extinfo:
    #         catid = rec_info.extinfo['def_cat_uid']
    #     else:
    #         catid = ''
    #
    #     if len(catid) == 4:
    #         pass
    #     else:
    #         catid = ''
    #
    #     catinfo = None
    #     p_catinfo = None
    #
    #     post2catinfo = MPost2Catalog.get_first_category(postinfo.uid)
    #     if post2catinfo:
    #         catid = post2catinfo.tag_id
    #         catinfo = MCategory.get_by_uid(catid)
    #         if catinfo:
    #             p_catinfo = MCategory.get_by_uid(catinfo.pid)
    #
    #     kwd = {
    #         'def_cat_uid': catid,
    #         'parentname': '',
    #         'catname': '',
    #         'parentlist': MCategory.get_parent_list(),
    #         'userip': self.request.remote_ip}
    #
    #     if self.filter_view:
    #         tmpl = 'autogen/edit/edit_{0}.html'.format(catid)
    #     else:
    #         tmpl = 'post_{0}/post_edit.html'.format(self.kind)
    #
    #     logger.info('Meta template: {0}'.format(tmpl))
    #
    #     self.render(tmpl,
    #                 kwd=kwd,
    #                 calc_info=rec_info,  # Deprecated
    #                 post_info=rec_info,  # Deprecated
    #                 app_info=rec_info,  # Deprecated
    #                 postinfo=rec_info,
    #                 catinfo=catinfo,
    #                 pcatinfo=p_catinfo,
    #                 userinfo=self.userinfo,
    #                 unescape=tornado.escape.xhtml_unescape,
    #                 cat_enum=MCategory.get_qian2(catid[:2]),
    #                 tag_infos=MCategory.query_all(by_order=True, kind=self.kind),
    #                 tag_infos2=MCategory.query_all(by_order=True, kind=self.kind),
    #                 app2tag_info=MPost2Catalog.query_by_entity_uid(infoid, kind=self.kind).naive(),
    #                 app2label_info=MPost2Label.get_by_uid(infoid, kind=self.kind + '1').naive())
    # @tornado.web.authenticated
    # def __to_add(self, **kwargs):
    #     '''
    #     Used for info1.
    #     '''
    #
    #     if 'catid' in kwargs:
    #         catid = kwargs['catid']
    #         return self.__to_add_with_category(catid)
    #
    #     else:
    #
    #         if self.check_post_role()['ADD']:
    #             pass
    #         else:
    #             return False
    #
    #         if 'uid' in kwargs and MPost.get_by_uid(kwargs['uid']):
    #             # todo:
    #             # self.redirect('/{0}/edit/{1}'.format(self.app_url_name, uid))
    #             uid = kwargs['uid']
    #         else:
    #             uid = ''
    #         self.render('post_{0}/post_add.html'.format(self.kind),
    #                     tag_infos=MCategory.query_all(by_order=True, kind=self.kind),
    #                     userinfo=self.userinfo,
    #                     kwd={'uid': uid, })

    def ext_view_kwd(self, postinfo):
        post_data = self.get_post_data()

        out_dic = {
            'marker': 1 if 'marker' in post_data else 0,
            'geojson': post_data['gson'] if 'gson' in post_data else '',
            'map_hist_arr': self.__extra_view(postinfo.uid)
        }
        if 'zoom' in post_data:
            out_dic['vzoom'] = post_data['zoom']
        if 'lat' in post_data:
            out_dic['vlat'] = post_data['lat']
        if 'lon' in post_data:
            out_dic['vlon'] = post_data['lon']

        return out_dic

    def __extra_view(self, app_id):
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

    def ext_tmpl_view(self, rec):
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

        MPost.update_jsonb(uid, post_data)


class MapLayoutHandler(BaseHandler):
    '''
    Layerout for map handler.
    '''

    def initialize(self):
        super(MapLayoutHandler, self).initialize()

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
        MLayout.delete(uid)

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
        MLayout.add_or_update(post_data)


class MapOverlayHandler(BaseHandler):
    '''
    For map overlay.
    '''

    def initialize(self):
        super(MapOverlayHandler, self).initialize()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if len(url_arr) > 1:
            self.show_overlay(url_arr)
        else:
            kwd = {'title': '',
                   'info': ''}
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
            c_ap = MPost.get_by_uid(app_rr)
            app_info_arr.append(c_ap)
            lon_arr.append(float(c_ap.extinfo['ext_lon']))
            lat_arr.append(float(c_ap.extinfo['ext_lat']))
            zoom_max_arr.append(int(c_ap.extinfo['ext_zoom_max']))
            zoom_min_arr.append(int(c_ap.extinfo['ext_zoom_min']))
            zoom_current_zrr.append(int(c_ap.extinfo['ext_zoom_current']))

        kwd = {'url': 1,
               'cookie_str': '',
               'lon': average_array(lon_arr),
               'lat': average_array(lat_arr),
               'zoom_max': max(zoom_max_arr),
               'zoom_min': min(zoom_min_arr),
               'zoom_current': int(average_array(zoom_current_zrr))}
        if 'fullscreen' in self.request.arguments:
            tmpl = 'post_m/overlay/overlay_full.html'
        else:
            tmpl = 'post_m/overlay/overlay.html'
        self.render(tmpl,
                    topmenu='',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    app_arr=app_info_arr,
                    app_str='/'.join(app_arr))
