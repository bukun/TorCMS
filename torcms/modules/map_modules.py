import tornado.web
# from config import app_url_name

from torcms.model.json_model import MJson
from torcms.model.layout_model import MLayout
import config

class app_json(tornado.web.UIModule):
    def render(self,  app_id,user_id):
        self.mjson = MJson()
        self.mlayout = MLayout()

        json_recs = self.mjson.query_by_app(app_id, user_id)

        print('map data count: ', json_recs.count())

        kwd = {
            'pager': '',
            'signature': app_id,
            'tdesc': '',
            'site_url': config.site_url,

        }

        return self.render_string('modules/map/map_json.html',
                                  json_recs = json_recs,
                                  app_id = app_id,
                                  kwd=kwd)

class app_layout(tornado.web.UIModule):
    def render(self, app_id, user_id):
        self.mlayout = MLayout()

        layout_recs = self.mlayout.query_by_app(app_id, user_id)

        print(layout_recs.count())

        kwd = {
            'pager': '',
            'tdesc': '',
            'site_url': config.site_url,

        }

        return self.render_string('modules/map/map_layout.html',
                                  layout_recs = layout_recs,
                                  kwd=kwd)
