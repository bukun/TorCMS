# -*- coding:utf-8 -*-
import torcms_maplet.handlers.geojson as geojson_control
import torcms_maplet.handlers.geojson_v2 as geojson_control_v2
import torcms_maplet.handlers.geojson_v3 as geojson_v3

# from torcms_maplet.handlers.geojson import GeoJsonHandler, GeoJsonAjaxHandler
from torcms_maplet.handlers.map_handler import MapPostHandler, MapLayoutHandler, MapOverlayHandler, \
    MapAdminHandler
from torcms_maplet.handlers.mapview_handler import MapViewHandler
from torcms_maplet.handlers.map_log_handler import MapLogHandler

_urls = [
    ('/overlay/(.*)', MapOverlayHandler, dict()),
    ('/mapview/(.*)', MapViewHandler, dict()),
    ('/map/overlay/(.*)', MapOverlayHandler, dict()),  # Deprecated, repaled by `/overlay/` .

    ('/admin_map/(.*)', MapAdminHandler, dict()),
    ("/map/(.*)", MapPostHandler, dict(kind='m')),

    # Using GeoJson.
    ('/geojson_v1/(.*)', geojson_control.GeoJsonHandler, dict()),
    ('/geojson_j_v1/(.*)', geojson_control.GeoJsonAjaxHandler, dict()),

    # WebDog MapEditor.
    ('/geojson/(.*)', geojson_control_v2.GeoJsonHandler, dict()),
    ('/geojson_v2/(.*)', geojson_control_v2.GeoJsonHandler, dict()),

    ('/geojson_j/(.*)', geojson_control_v2.GeoJsonAjaxHandler, dict()),
    ('/geojson_j_v2/(.*)', geojson_control_v2.GeoJsonAjaxHandler, dict()),

    ('/mapdraw_v3/(.*)', geojson_v3.GeoJsonHandler, dict()),
    ('/mapdraw_j_v3/(.*)', geojson_v3.GeoJsonAjaxHandler, dict()),
    ('/layout/(.*)', MapLayoutHandler, dict()),

    ("/map_log/(.*)", MapLogHandler, dict()),

]
