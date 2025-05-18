# -*- coding:utf-8 -*-

'''
define the Core Modules of TorCMS.
'''

from torcms_maplet.modules import map_modules

_modules = {
    # Map
    'app_layout': map_modules.MapLayout,
    'app_json': map_modules.MapJson,
    'map_ad': map_modules.MapAd,
}
