LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (43.88, 125.35),  # Center of Washington, D.C.
    'DEFAULT_ZOOM': 10,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
    'SCALE': 'both',
    'ATTRIBUTION_PREFIX': 'Leaflet',
    'PLUGINS': {
        'leaflet-geoman': {
            'js': ['leaflet-geoman.js'],
            'css': ['leaflet-geoman.css'],
            'auto-css': True,
            'auto-js': True,
        },
        'fullscreen': {  # 启用全屏插件
            'js': 'https://cdn.jsdelivr.net/npm/leaflet-fullscreen@1.0.2/dist/Leaflet.fullscreen.min.js',
            'css': 'https://cdn.jsdelivr.net/npm/leaflet-fullscreen@1.0.2/dist/leaflet.fullscreen.min.css',
            'auto-include': True,
            'priority': 100,
        },
        'search': {  # 启用搜索插件
            'js': ['my_custom_search_plugin.js'],  # 自定义搜索插件的JS文件
            'css': ['my_custom_search_plugin.css'],  # 自定义搜索插件的CSS文件
            'autoCollapse': True,  # 当地图移动时是否自动折叠搜索控件
            'collapsed': False,  # 是否在加载时折叠搜索控件
            'position': 'topleft',  # 搜索控件在地图上的位置
            'providers': [
                {  # 提供搜索结果的提供者，例如使用OpenStreetMap Nominatim服务
                    'osm': {
                        'label': 'OpenStreetMap',
                        'url': 'https://nominatim.openstreetmap.org/search/{query}?format=json',
                        'bounds': [[-90.0, -180.0], [90.0, 180.0]],
                        'polygon_true': '1',
                        'polygon_false': '0',
                        'polygon_threshold': 0.1,
                        'limit': 5,
                    }
                }
            ],
        },
    },
    'TILES': [
        (
            'OpenStreetMap.DE',
            'http://tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png',
            {
                'type': 'sat',
                'ext': 'jpg',
                'attribution': 'Data CC-By-SA by <a href="http://openstreetmap.org/" target="_blank">OpenStreetMap</a>, Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a>',
                'subdomains': ['1', '2', '3', '4'],
            },
        ),
        (
            'OpenStreetMap.BlackAndWhite',
            'http://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png',
            {
                'type': 'sat',
                'ext': 'jpg',
                'attribution': 'Data CC-By-SA by <a href="http://openstreetmap.org/" target="_blank">OpenStreetMap</a>, Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a>',
                'subdomains': ['1', '2', '3', '4'],
            },
        ),
        (
            'OpenStreetMap.Mapnik',
            'http://tile.openstreetmap.org/{z}/{x}/{y}.png',
            {
                'type': 'sat',
                'ext': 'jpg',
                'attribution': 'Data CC-By-SA by <a href="http://openstreetmap.org/" target="_blank">OpenStreetMap</a>, Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a>',
                'subdomains': ['1', '2', '3', '4'],
            },
        ),
    ],
    # 'TILES': [('Aerial Imagery', 'http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
    #            {'type': 'sat', 'ext': 'jpg',
    #             'attribution': 'Data CC-By-SA by <a href="http://openstreetmap.org/" target="_blank">OpenStreetMap</a>, Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a>',
    #             'subdomains': ['1', '2', '3', '4']})],
}
