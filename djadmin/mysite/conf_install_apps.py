INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # 多站点配置

    'oauth2_provider',
    'django.contrib.gis',
    'rest_framework',
    'rest_framework_gis',
    'import_export',
    'django_filters',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    'mdeditor',
    'leaflet',
    'geoposition',

    'django_comments',
    # 'crequest',
    'mptt',
    'friendship',

    "wagtail_dir.wagtail_blog",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",

    'users',
    'bootstrap4',
    'data.categorys',
    'data.labels',
    'data.map',
    'data.dataset',

    'igais.igais_category',
    'igais.igais_label',
    'igais.igais_data',

    'qgis.heitu_map_category',
    'qgis.zhongmeng_map_category',
    'qgis.yaou_map_category',
    'qgis.zhongba_map_category',
    'qgis.anso_map_category',
    'qgis.bigscreen_map_category',
    'qgis.qgis_label',
    'qgis.vector_layer',
    'qgis.qgis_map',

    'post.doc_category',
    'post.doc_label',
    'post.document',
    'post.topic',

    'apiapp',

    'crawl.crawl_label',
    'crawl.crawl_source',
    'crawl.crawl_document',
    'crawl.crawl_document_en',

    'world',

    # 专题资源管理
    'dresource.resource_category',
    'dresource.resource_label',
    'dresource.resource_dataset',

    # 翻译库
    'translation_library.trans_en_zh',
    'translation_library.trans_zh_en',
    # 地名库
    'place.place_name',
    'place.linear_features',
    'place.planar_features',

    'place.geofea',  # http://geofea.gislab.cn/#/html/index/
    'place.thematic_maps',
    'place.test_text',
    'place.geopage',
    'place.xzqh',

    'place.photo_info',

    # 长春工程建设管理：（文字识别结果）
    'changchun_project',
    # 中南专栏

    'zhongnan.zn_dataset_category',
    'zhongnan.zn_dataset_label',
    'zhongnan.zn_dataset',

    'zhongnan.zn_event_category',
    'zhongnan.zn_event_label',
    'zhongnan.zn_event',

    # 黑土粮仓

    'heitu_barn.barn_device',
    'heitu_barn.barn_field',
    'heitu_barn.device_soilmoisture',
    'heitu_barn.device_soilfiveparameters',
    'heitu_barn.device_soilfiveparametersv2',
    'heitu_barn.device_meteorology',
    'heitu_barn.barn_dataset',

    # 在线制图与编辑应用系统
    'layerstyle.lgeojson',
    'layerstyle.lprogram',

    'jupyters.jupyter_category',  # 科学计算模型分类
    'jupyters.jupyter_data',  # 科学计算模型数据

    'literature.literature_category',  # 文献分类
    'literature.literature_label',  # 文献标签
    'public_model.public_country',  # 国家库
    'public_model.literature_author',  # 作者库
    'public_model.literature_date',  # 日期库
    'literature.literature_data',  # 文献库

    'pages.page',
    'pages.wiki',
    'bigscreen.bigscreen_data',  # 大屏数据
    'bigscreen.jump_btn',  # 大屏数据

    'black_html.sphinx_doc',  # sphinx

    'yaou_data_categorys.Basic_Geographic_Element',  # 亚欧大陆数据分类
    'public_model.portal_index',  # 各个门户网站首页

    # iga办公室信息
    'iga.iga_group', # 学科组
    'iga.iga_room', # 办公室信息
    'iga.iga_staff', # 人员
    'iga.iga_floor', # 楼层
]