from django.utils.translation import gettext_lazy as _

SIMPLEUI_LOGO = 'https://oss.cuiliangblog.cn/image/logo.png'
# 隐藏首页的快捷操作和最近动作
# SIMPLEUI_HOME_QUICK = False
# SIMPLEUI_HOME_ACTION = False
# 隐藏右侧SimpleUI广告链接和使用分析
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
# 设置右上角Home图标跳转链接，会以另外一个窗口打开
SIMPLEUI_INDEX = '/'

# SIMPLEUI_HOME_PAGE = '/xzqh/map_view/'
# SIMPLEUI_HOME_TITLE = '控制面板!'
# SIMPLEUI_HOME_ICON = 'fa fa-eye'


# 当然使用SimpleUI系统菜单也有优点，比如用户拥有什么模型的权限就显示什么菜单。自定义menus中输出的菜单不会受权限控制。如果你想要在后台使用基于RBAC控制的菜单，就不要通过SIMPLEUI_CONFIG自定义菜单
#
MENUS = [
    {
        'app': 'users',
        'name': '后台组织管理',
        'name_en': 'Backend',
        'icon': 'fas fa-user-shield',
        'models': [
            {
                'name': '角色管理',
                'name_en': 'Role Management',
                'icon': 'fa fa-th-list',
                'url': '/admin/users/admingroup/'
            },
            {
                'name': '用户管理',
                'icon': 'fa fa-user',
                'url': '/admin/users/myuser/'
            },
            {
                'name': '站点管理',
                'icon': 'fas fa-globe-americas',
                'url': '/admin/sites/site/'
            },

        ]
    },

    {
        'name': "数据管理",
        'name_en': 'Data Management',
        'icon': 'fa fa-th-list',
        'models': [

            {
                'name': '分类管理',
                'url': '/admin/categorys/categorys/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '标签管理',
                'url': '/admin/labels/labels/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '数据管理',
                'url': '/admin/dataset/dataset/',
                'icon': 'fa fa-tasks'
            },

            {
                'name': '数据地图',
                'url': '/admin/map/map/',
                'icon': 'fa fa-tasks'
            },
            # {
            #     'name': '全球地图',
            #     'url': '/admin/world/world/',
            #     'icon': 'fa fa-tasks'
            # },
        ]
    },
    {
        'name': '科学计算模型管理',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': '科学计算模型分类',
                'url': '/admin/jupyter_category/jupytercatagory/',
                'icon': 'fa fa-tasks'
            },

            {
                'name': '科学计算模型数据',
                'url': '/admin/jupyter_data/jupyter/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '分享给我的数据',
                'url': '/jupyter_data/show_share/',
                'icon': 'fa fa-tasks'
            },

        ]
    },
    {
        'name': '公共模型管理',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': '国家库管理',
                'url': '/admin/public_country/publiccountry/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '作者库管理',
                'url': '/admin/literature_author/literatureauthor/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '日期库管理',
                'url': '/admin/literature_date/literaturedate/',
                'icon': 'fa fa-tasks'
            },

        ]
    },
    {
        'name': '文献管理',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': '文献分类',
                'url': '/admin/literature_category/literaturecatagory/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '文献标签',
                'url': '/admin/literature_label/literaturelabel/',
                'icon': 'fa fa-tasks'
            },

            {
                'name': '文献数据',
                'url': '/admin/literature_data/literature/',
                'icon': 'fa fa-tasks'
            },

        ]
    },

    {
        'name': '地图管理',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': 'QGIS地图',
                'url': '/admin/qgis_map/qgismap/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '矢量图层管理',
                'url': '/admin/vector_layer/vectorlayer/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': 'QGIS地图标签',
                'url': '/admin/qgis_label/qgislabel/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '黑土地图分类',
                'url': '/admin/heitu_map_category/heitumapcategory/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '色楞格河地图分类',
                'url': '/admin/zhongmeng_map_category/zhongmengmapcategory/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '亚欧地图分类',
                'url': '/admin/yaou_map_category/yaoumapcategory/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '中巴地图分类',
                'url': '/admin/zhongba_map_category/zhongbamapcategory/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': 'ANSO地图分类',
                'url': '/admin/anso_map_category/ansomapcategory/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '大屏地图分类',
                'url': '/admin/bigscreen_map_category/bigscreenmapcategory/',
                'icon': 'fa fa-tasks'
            },

        ]
    },
    {
        'name': '大屏管理',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': '大屏数据管理',
                'url': '/admin/bigscreen_data/bigscreendata/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '跳转按钮管理',
                'url': '/admin/jump_btn/jumpbtn/',
                'icon': 'fa fa-tasks'
            },

        ]
    },
    {
        'name': 'Igais管理',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': '分类管理',
                'url': '/admin/igais_category/igaiscategory/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '标签管理',
                'url': '/admin/igais_label/igaislabel/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '数据管理',
                'url': '/admin/igais_data/igaisdata/',
                'icon': 'fa fa-tasks'
            },
            # {
            #     'name': '农产品最新价格',
            #     'url': '/admin/farmpro/farmpro/',
            #     'icon': 'fa fa-tasks'
            # },
            # {
            #     'name': '农产品地区均价',
            #     'url': '/admin/farmpro_avg/farmproavg/',
            #     'icon': 'fa fa-tasks'
            # },
        ]
    },
    {
        'name': '文档管理',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': '分类管理',
                'url': '/admin/doc_category/documentcatagory/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '标签管理',
                'url': '/admin/doc_label/doclabel/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '文档管理',
                'url': '/admin/document/document/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '协同计算?问答',
                'icon': 'fa fa-th-list',
                'models': [
                    {
                        'name': '问答',
                        'url': '/admin/topic/topic/',
                        'icon': 'fa fa-tasks'
                    },
                    {
                        'name': 'comment',
                        'url': '/admin/topic/comment/',
                        'icon': 'fa fa-tasks'
                    },

                ]
            },

        ]
    },
    {
        'name': '单页管理',
        'icon': 'fa fa-th-list',
        'models': [

            {
                'name': '单页管理',
                'url': '/admin/page/page/',
                'icon': 'fa fa-tasks'
            },

        ]
    },
    {
        'name': '爬取数据管理',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': '数据来源',
                'url': '/admin/crawl_source/crawlsource/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '数据分类',
                'url': '/admin/crawl_label/crawllabel/',
                'icon': 'fa fa-tasks'
            },

            {
                'name': '中文数据管理',
                'url': '/admin/crawl_document/crawldocument/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '英文数据管理',
                'url': '/admin/crawl_document_en/crawldocumenten/',
                'icon': 'fa fa-tasks'
            },
            # {
            #     'name': '修改日志',
            #     'url': '/admin/crawl_document_en/rzlog/',
            #     'icon': 'fa fa-tasks'
            # }

        ]
    },

    {
        'name': '专题资源管理',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': '标签管理',
                'url': '/admin/resource_label/resourcelabel/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '软件分类管理',
                'url': '/admin/resource_category/resourcecatagory/',
                'icon': 'fa fa-tasks'
            },

            {
                'name': '软件资源管理',
                'url': '/admin/resource_dataset/resource/',
                'icon': 'fa fa-tasks'
            },

        ]
    },
    {
        'name': '翻译库管理',
        'icon': 'fa fa-th-list',
        'models': [

            {
                'name': '英-中翻译管理',
                'url': '/admin/trans_en_zh/translationenzh/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '中-英翻译管理',
                'url': '/admin/trans_zh_en/translationzhen/',
                'icon': 'fa fa-tasks'
            },

        ]
    },
    {
        'name': '地名库管理',
        'icon': 'fa fa-th-list',
        'models': [

            {
                'name': '地名库管理',
                'url': '/admin/place_name/placename/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '线状要素库',
                'url': '/admin/linear_features/linearfeatures/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '面状要素库',
                'url': '/admin/planar_features/planarfeatures/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': 'Geofea管理',
                'icon': 'fa fa-th-list',
                'url': '/admin/geofea/geofea/'
            },
            {
                'name': '专题地图',
                'url': '/admin/thematic_maps/thematicmaps/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '测试文本',
                'icon': 'fa fa-th-list',
                'url': '/admin/test_text/testtext/'
            },
            {
                'name': '地名页面',
                'icon': 'fa fa-th-list',
                'url': '/admin/geopage/geopage/'
            },
            {
                'name': '行政区划',
                'icon': 'fa fa-th-list',
                'url': '/admin/xzqh/xzqh/'
            },
            {
                'name': '照片信息',
                'icon': 'fa fa-th-list',
                'url': '/admin/photo_info/photoinfo/'
            },

        ]
    },

    {
        'app': 'changchun_project',
        'name': '特别专题',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': '长春工程管理',
                'icon': 'fa fa-th-list',
                'url': '/admin/changchun_project/changchunproject/'
            },

            {
                'name': '亚欧大陆分类表基础地理要素数据指标分类',
                'url': '/admin/Basic_Geographic_Element/basic_geographic_element_category/',
                'icon': 'fa fa-tasks'
            },

        ]
    },



    {
        'name': '中南专栏',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': '数据管理',
                'icon': 'fa fa-tasks',
                'models': [
                    {
                        'name': '数据标签',
                        'name_en': 'Data Labels',
                        'url': '/admin/zn_dataset_label/zndatasetlabel/',
                        'icon': 'fa fa-tasks'
                    },
                    {
                        'name': '数据分类',
                        'url': '/admin/zn_dataset_category/zndatasetcategory/',
                        'icon': 'fa fa-tasks'
                    },
                    {
                        'name': '数据列表',
                        'url': '/admin/zn_dataset/zndataset/',
                        'icon': 'fa fa-tasks'
                    },

                ]
            },

            {
                'name': '事件管理',
                'icon': 'fa fa-tasks',
                'models': [
                    {
                        'name': '事件标签',
                        'url': '/admin/zn_event_label/zneventlabel/',
                        'icon': 'fa fa-tasks'
                    },
                    {
                        'name': '事件分类',
                        'url': '/admin/zn_event_category/zneventcategory/',
                        'icon': 'fa fa-tasks'
                    },
                    {
                        'name': '事件列表',
                        'url': '/admin/zn_event/znevent/',
                        'icon': 'fa fa-tasks'
                    },

                ]
            },

        ]
    },
    {
        'name': '黑土粮仓数据管理',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': '农业站数据管理',
                'icon': 'fa fa-th-list',
                'models': [
                    {
                        'name': '照片管理',
                        'url': '/admin/barn_dataset/barndataset/',
                        'icon': 'fa fa-tasks'
                    },
                    {
                        'name': '设备管理',
                        'url': '/admin/barn_device/barndevice/',
                        'icon': 'fa fa-tasks'
                    },
                    {
                        'name': '田块管理',
                        'url': '/admin/barn_field/barnfield/',
                        'icon': 'fa fa-tasks'
                    },
                ]
            },
            {
                'name': '农业站气象站数据管理',
                'icon': 'fa fa-th-list',
                'models': [
                    {
                        'name': '土壤水分监测',
                        'url': '/admin/device_soilmoisture/devicesoilmoisture/',
                        'icon': 'fa fa-tasks'
                    },
                    {
                        'name': '土壤五参数1',
                        'url': '/admin/device_soilfiveparameters/soilfivepara1/',
                        'icon': 'fa fa-tasks'
                    },
                    {
                        'name': '土壤五参数2',
                        'url': '/admin/device_soilfiveparametersv2/soilfiveparav2/',
                        'icon': 'fa fa-tasks'
                    },
                    {
                        'name': '全自动气象站',
                        'url': '/admin/device_meteorology/meteorology/',
                        'icon': 'fa fa-tasks'
                    },
                ]
            },

        ]
    },

    {
        'name': '在线制图数据管理',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': 'GeoJSON地理数据',
                'url': '/admin/lgeojson/lgeojson/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '项目管理',
                'url': '/admin/lprogram/lprogram/',
                'icon': 'fa fa-tasks'
            },

        ]
    },

    {
        'name': ' Django OAuth Toolkit',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': 'Access tokens',
                'url': '/admin/oauth2_provider/accesstoken/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': 'Applications',
                'url': '/admin/oauth2_provider/application/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': 'Grants',
                'url': '/admin/oauth2_provider/grant/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': 'Id tokens',
                'url': '/admin/oauth2_provider/idtoken/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': 'Refresh tokens',
                'url': '/admin/oauth2_provider/refreshtoken/',
                'icon': 'fa fa-tasks'
            },

        ]
    },
    {
        'name': '好友管理',
        'icon': 'fa fa-th-list',
        'models': [
            {
                'name': '屏蔽关系',
                'url': '/admin/friendship/block/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '关注关系',
                'url': '/admin/friendship/follow/',
                'icon': 'fa fa-tasks'
            },

            {
                'name': '好友列表',
                'url': '/admin/friendship/friend/',
                'icon': 'fa fa-tasks'
            },
            {
                'name': '好友请求',
                'url': '/admin/friendship/friendshiprequest/',
                'icon': 'fa fa-tasks'
            },

        ]
    },
]

for app in MENUS:
    if 'name_en' in app:
        app['name'] = app['name_en']
    for model in app['models']:
        if 'name_en' in model:
            model['name'] = model['name_en']
        if 'models' in model:
            for sub_model in model['models']:
                if 'name_en' in sub_model:
                    sub_model['name'] = sub_model['name_en']


SIMPLEUI_CONFIG = {
    # 是否使用系统默认菜单，自定义菜单时建议关闭。
    'system_keep': False,

    # # 用于菜单排序和过滤, 不填此字段为默认排序和全部显示。空列表[] 为全部不显示.
    # 'menu_display': ['后台组织管理', '前台用户管理', '黑土管理', '数据管理', '地图管理', 'Igais管理',
    #                  '文档管理', '爬取数据管理', 'WDC-RRE', '专题资源管理', '翻译库管理', '地名库管理','长春工程管理','中南专栏'],

    # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时刷新展示菜单内容。
    # 一般建议关闭。
    'dynamic': True,
    'menus': MENUS
}
