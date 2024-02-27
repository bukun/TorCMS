# -*- coding:utf-8 -*-

'''
Handlers for Map application.
'''
import random
import time
from pathlib import Path
import os
import tornado.web
import config
from config import post_cfg
from torcms.core.base_handler import BaseHandler
from torcms.handlers.post_handler import PostHandler
from torcms.model.post_model import MPost
from torcms_maplet.model.layout_model import MLayout
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.label_model import MPost2Label
from torcms.core.tools import logger
from torcms.model.usage_model import MUsage
from torcms.core.tool.sqlite_helper import MAcces
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
        # print('from map post get')
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

        elif len(url_arr) == 1 and url_str.endswith('.html'):
            # Deprecated
            self.redirect('/post/{uid}'.format(uid=url_str.split('.')[0]))
        elif len(url_arr) == 1 and len(url_str) in [4]:
            self.redirect('/map/m' + url_str)
        elif len(url_arr) == 1 and len(url_str) in [5]:
            self._view_or_add(url_str)
        else:
            kwd = {
                'title': '',
                'info': '404. Page not found!',
            }
            self.set_status(404)
            self.render('misc/html/404.html', kwd=kwd,
                        userinfo=self.userinfo )

    def ext_view_kwd(self, postinfo):
        post_data = self.get_request_arguments()
        # print('=|' * 40)
        # print(post_data['extinfo)

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
        try:
            if config.wcs_svr:
                out_dic['wcs_svr'] = config.wcs_svr
        except Exception:
            out_dic['wcs_svr'] = 'http://wcs.osgeo.cn'
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
    def viewinfo(self, postinfo):
        '''
        查看 Post.
        '''



        __ext_catid = postinfo.extinfo.get('def_cat_uid', '')
        cat_enum1 = MCategory.get_qian2(__ext_catid[:2]) if __ext_catid else []
        rand_recs, rel_recs = self.fetch_additional_posts(postinfo.uid)

        self._chuli_cookie_relation(postinfo.uid)

        catinfo = None
        p_catinfo = None

        post2catinfo = MPost2Catalog.get_first_category(postinfo.uid)

        if post2catinfo:
            catinfo = MCategory.get_by_uid(post2catinfo.tag_id)
            if catinfo:
                p_catinfo = MCategory.get_by_uid(catinfo.pid)

        else:
            print('无信息')
        kwd = self._the_view_kwd(postinfo)

        MPost.update_misc(postinfo.uid, count=True)
        MAcces.add(postinfo.uid)

        if self.get_current_user() and self.userinfo:
            MUsage.add_or_update(self.userinfo.uid, postinfo.uid, postinfo.kind)

        self.set_cookie('user_pass', kwd['cookie_str'])

        tmpl = self.ext_tmpl_view(postinfo)

        if self.userinfo:
            recent_apps = MUsage.query_recent(
                self.userinfo.uid, postinfo.kind, 6
            ).objects()[1:]
        else:
            recent_apps = []
        logger.info('The Info Template: {0}'.format(tmpl))

        if self.cache:
            result = self.render_string(
                tmpl,
                kwd=dict(kwd, **self.ext_view_kwd(postinfo)),
                postinfo=postinfo,
                userinfo=self.userinfo,
                catinfo=catinfo,
                pcatinfo=p_catinfo,
                relations=rel_recs,
                rand_recs=rand_recs,
                subcats=MCategory.query_sub_cat(p_catinfo.uid) if p_catinfo else '',
                ad_switch=random.randint(1, 18),
                tag_info=filter(
                    lambda x: not x.tag_name.startswith('_'),
                    MPost2Label.get_by_uid(postinfo.uid).objects(),
                ),
                recent_apps=recent_apps,
                cat_enum=cat_enum1,
                router=post_cfg[catinfo.kind]['router'],
                post_type=post_cfg[catinfo.kind].get('show', post_cfg[catinfo.kind].get('router')),
            )



        # self.render(f'caches/{cache_file.name}')

        self.render(
            tmpl,
            kwd=dict(kwd, **self.ext_view_kwd(postinfo)),
            postinfo=postinfo,
            userinfo=self.userinfo,
            catinfo=catinfo,
            pcatinfo=p_catinfo,
            relations=rel_recs,
            rand_recs=rand_recs,
            subcats=MCategory.query_sub_cat(p_catinfo.uid) if p_catinfo else '',
            ad_switch=random.randint(1, 18),
            tag_info=filter(
                lambda x: not x.tag_name.startswith('_'),
                MPost2Label.get_by_uid(postinfo.uid).objects(),
            ),
            recent_apps=recent_apps,
            cat_enum=cat_enum1,
            router=post_cfg[catinfo.kind]['router'],
            post_type=post_cfg[catinfo.kind].get('show', post_cfg[catinfo.kind].get('router')),
        )
    def ext_tmpl_view(self, rec):
        if 'fullscreen' in self.request.arguments:
            if 'version' in self.request.arguments:
                tmpl = '../torcms_maplet/tmpl/full_screen_v2.html'.format(self.kind)
            else:
                tmpl = '../torcms_maplet/tmpl/full_screen.html'.format(self.kind)
        elif 'view3d' in self.request.arguments:
            tmpl = '../torcms_maplet/tmpl/view3d.html'.format(self.kind)
        else:
            tmpl = 'post_m/show_map.html'.format(self.kind)
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
        post_data = self.get_request_arguments()

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
        '''
        MLayout.delete(uid)

    @tornado.web.authenticated
    def save_layout(self):
        '''
        Save the map layout.
        '''
        post_data = self.get_request_arguments()
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
        self.redirect('/mapview/overlay/' + url_str)

        # if len(url_arr) > 1:
        #
        #     self.show_overlay(url_arr)
        # else:
        #     kwd = {'title': '',
        #            'info': ''}
        #     self.render('misc/html/404.html',
        #                 kwd=kwd,
        #                 userinfo=self.userinfo)
