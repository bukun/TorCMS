# coding:utf-8

from torcms.model.infor2label_model import MInfor2Label
from torcms.model.info_model import MInfor
from torcms.model.info_relation_model import MInforRel
from torcms.model.evaluation_model import MEvaluation
from torcms.model.category_model import MCategory
from torcms.model.usage_model import MUsage
from torcms.model.infor2catalog_model import MInfor2Catalog
from torcms.handlers.info_handler import InfoHandler
from torcms.model.info_hist_model import MInfoHist


class MapPostHandler(InfoHandler):
    def initialize(self, **kwargs):
        super(MapPostHandler, self).initialize()
        self.mevaluation = MEvaluation()
        self.mpost2catalog = MInfor2Catalog()
        self.mpost2label = MInfor2Label()
        self.mpost_hist = MInfoHist()
        self.minfor = MInfor()
        self.musage = MUsage()
        self.mcat = MCategory()
        self.mrel = MInforRel()
        if 'kind' in kwargs:
            self.kind = kwargs['kind']
        else:
            self.kind = '9'

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
            for xx in range(0, len(self.get_secure_cookie('map_hist').decode('utf-8')), 4):
                map_hist.append(self.get_secure_cookie('map_hist').decode('utf-8')[xx: xx + 4])
        return map_hist

    def ext_tmpl_name(self, rec):
        if 'fullscreen' in self.request.arguments:
            tmpl = 'post_{0}/full_screen.html'.format(self.kind)
        else:
            tmpl = 'post_{0}/show_map.html'.format(self.kind)
        return tmpl


class MapAdminHandler(MapPostHandler):
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
