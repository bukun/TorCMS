"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
from cfg import DB_INFO, CACHES_INFO

from django.views.generic import TemplateView

import os

WAGTAIL_SITE_NAME = 'WAGTAIL ADMIN'
SITE_ID = int(os.environ.get('SITE_ID', 1))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2@0v#aiu_edfdl2z286icz7r)_u&bua%f3f@b2$+#_yw$-a1p5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
AUTH_USER_MODEL = 'users.MyUser'
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),  # access有效时间
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # refresh有效时间
    'ROTATE_REFRESH_TOKENS': True,
}
LOGOUT_REDIRECT_URL = "/admin/"
# Application definition

# 访问django后台，提示CSRF验证失败. 请求被中断.
# https://blog.csdn.net/weixin_37770279/article/details/124480045 
CSRF_TRUSTED_ORIGINS = ['https://cms.igadc.cn']

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
    'data.dataset',
    'data.map',

    'igais.igais_category',
    'igais.igais_label',
    'igais.igais_data',

    'qgis.qgis_map',
    'qgis.heitu_map_category',
    'qgis.zhongmeng_map_category',
    'qgis.yaou_map_category',
    'qgis.zhongba_map_category',
    'qgis.anso_map_category',
    'qgis.bigscreen_map_category',
    'qgis.qgis_label',
    'qgis.vector_layer',

    'post.doc_category',
    'post.doc_label',
    'post.document',
    'post.topic',

    'apiapp',

    'crawl.crawl_label',
    'crawl.crawl_document',
    'crawl.crawl_document_en',
    'crawl.crawl_source',

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

    # 长春工程建设管理：（文字识别结果）
    'changchun_project',
    # 中南专栏
    'zhongnan.zn_dataset',
    'zhongnan.zn_dataset_category',
    'zhongnan.zn_dataset_label',
    'zhongnan.zn_event',
    'zhongnan.zn_event_category',
    'zhongnan.zn_event_label',

    # 黑土粮仓
    'heitu_barn.barn_dataset',
    'heitu_barn.barn_device',
    'heitu_barn.barn_field',
    'heitu_barn.device_soilmoisture',
    'heitu_barn.device_soilfiveparameters',
    'heitu_barn.device_soilfiveparametersv2',
    'heitu_barn.device_meteorology',

    # 在线制图与编辑应用系统
    'layerstyle.lgeojson',
    'layerstyle.lprogram',

    'jupyters.jupyter_data',  # 科学计算模型数据
    'jupyters.jupyter_category',  # 科学计算模型分类
    'literature.literature_category',  # 文献分类
    'literature.literature_label',  # 文献标签
    'literature.literature_data',  # 文献库
    'literature.literature_author',  # 文献作者库
    'literature.literature_date',  # 文献日期库

    'pages.page',
    'bigscreen.bigscreen_data',  # 大屏数据
    'bigscreen.jump_btn',  # 大屏数据

    'black_html.sphinx_doc', #sphinx
]

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
            'providers': [{  # 提供搜索结果的提供者，例如使用OpenStreetMap Nominatim服务
                'osm': {
                    'label': 'OpenStreetMap',
                    'url': 'https://nominatim.openstreetmap.org/search/{query}?format=json',
                    'bounds': [[-90.0, -180.0], [90.0, 180.0]],
                    'polygon_true': '1',
                    'polygon_false': '0',
                    'polygon_threshold': 0.1,
                    'limit': 5,
                }
            }],
        },
    },
    'TILES': [
        (
            'OpenStreetMap.DE',
            'http://tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png',
            {'type': 'sat', 'ext': 'jpg',
             'attribution': 'Data CC-By-SA by <a href="http://openstreetmap.org/" target="_blank">OpenStreetMap</a>, Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a>',
             'subdomains': ['1', '2', '3', '4']}
        ),
        (
            'OpenStreetMap.BlackAndWhite',
            'http://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png',
            {'type': 'sat', 'ext': 'jpg',
             'attribution': 'Data CC-By-SA by <a href="http://openstreetmap.org/" target="_blank">OpenStreetMap</a>, Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a>',
             'subdomains': ['1', '2', '3', '4']}
        ),
        (
            'OpenStreetMap.Mapnik',
            'http://tile.openstreetmap.org/{z}/{x}/{y}.png',
            {'type': 'sat', 'ext': 'jpg',
             'attribution': 'Data CC-By-SA by <a href="http://openstreetmap.org/" target="_blank">OpenStreetMap</a>, Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a>',
             'subdomains': ['1', '2', '3', '4']}
        ),

    ],
    # 'TILES': [('Aerial Imagery', 'http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
    #            {'type': 'sat', 'ext': 'jpg',
    #             'attribution': 'Data CC-By-SA by <a href="http://openstreetmap.org/" target="_blank">OpenStreetMap</a>, Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a>',
    #             'subdomains': ['1', '2', '3', '4']})],
}

MDEDITOR_CONFIGS = {
    'default': {
        'width': '100%',  # 自定义编辑框宽度
        'heigth': 500,  # 自定义编辑框高度

        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime",
                    "emoji", "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # 自定义编辑框工具栏

        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # 图片上传格式类型
        'image_folder': 'editor',  # 图片保存文件夹名称
        'theme': 'default',  # 编辑框主题 ，dark / default
        'preview_theme': 'default',  # 预览区域主题， dark / default
        'editor_theme': 'default',  # edit区域主题，pastel-on-dark / default
        'toolbar_autofixed': True,  # 工具栏是否吸顶
        'search_replace': True,  # 是否开启查找替换
        'emoji': True,  # 是否开启表情功能
        'tex': True,  # 是否开启 tex 图表功能
        'flow_chart': True,  # 是否开启流程图功能
        'sequence': True,  # 是否开启序列图功能
        'watch': True,  # 实时预览
        'lineWrapping': True,  # 自动换行
        'lineNumbers': False  # 行号
    },
}
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
# 设置文件上传处理器
FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]
MPTT_COMMENTS_ALLOW_ANONYMOUS = True  # True 为允许匿名评论，否则不允许

# CACHES = CACHES_INFO
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 引擎（默认）
# SESSION_COOKIE_NAME = "sessionid"  # Session的cookie保存在浏览器上时的key，
# SESSION_COOKIE_PATH = "/"  # Session的cookie保存的路径（默认）
# SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名（默认）
# SESSION_COOKIE_SECURE = False  # 是否Https传输cookie（默认）
# SESSION_COOKIE_HTTPONLY = True  # 是否Session的cookie只支持http传输（默认）
# SESSION_COOKIE_AGE = 60 * 30  # Session的cookie失效日期（30min）（默认）
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 是否关闭浏览器使得Session过期（默认）
# SESSION_SAVE_EVERY_REQUEST = True  # 是否每次请求都保存Session，默认修改之后才保存

IMPORT_EXPORT_USE_TRANSACTIONS = True
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # 使用OAuth登录认证

    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',

    ],
    # # 全局使用限流类
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '30/min',
    #     'user': '50/min'
    # },
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',  # 注意顺序
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',

]
# 即为可供资源拥有者(Django User)选择的 当第三方网站调用该网站资源时获取的权限范围。

OAUTH2_PROVIDER = {
    # OIDC 的配置。如果要用，须得在 JupyterHub 中对应配置。目前未成功。
    "OIDC_ENABLED": False,
    "PKCE_REQUIRED": False,
    "SCOPES": {
        "openid": "OpenID scope",
        "read": "Read scope",
        "write": "Write scope",
        "groups": "Access to your groups",
    },
}
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "oauth2_provider.backends.OAuth2Backend",
)

X_FRAME_OPTIONS = 'SAMEORIGIN'
ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 设置模板目录
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },

    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    },
#    'OPTIONS': {
#        'timeout': 20,
#    }
# }

DATABASES = {
    'default': DB_INFO
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

USE_L10N = True  # 默认False，以本地化格式显示数字和时间

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),
                    os.path.join(BASE_DIR, 'yy_static_html'),
                    ]

MEDIA_ROOT = os.path.join(BASE_DIR, 'yy_media')  # 上传图片的根目录

# 部署环境静态文件目录
STATIC_ROOT = os.path.join(BASE_DIR, 'xx_static')

MEDIA_URL = '/'
CKEDITOR_UPLOAD_PATH = 'upload/'
CKEDITOR_IMAGE_BACKEND = 'PIL'
# CKEDITOR_CONFIGS = {
#     'default': {
#         'skin': 'moono-lisa',
#         'toolbar_Basic': [
#             ['Source', '-', 'Bold', 'Italic']
#         ],
#         'toolbar_Full': [
#             [ 'Source','-','Save','NewPage','DocProps','Preview','Print','-','Templates' ],
#             [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ],
#
#             [ 'Find','Replace','-','SelectAll','-','SpellChecker', 'Scayt' ],
#             [ 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField' ],
#             '/',
#             [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ],
#             [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv', '-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ],
#             [ 'Link','Unlink','Anchor' ],
#             [ 'Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak','Iframe' ],
#             '/',
#             [ 'Styles','Format','Font','FontSize' ] ,
#             [ 'TextColor','BGColor' ] ,
#             [ 'Maximize', 'ShowBlocks','-','About' ] ,
#             ['CodeSnippet'],  #代码段按钮
#
#         ],
#         'toolbar': 'Full',
#         'extraPlugins': ','.join(['codesnippet', 'prism', 'widget', 'lineutils']),   #代码段插件
#     }
# }

CKEDITOR_CONFIGS = {

    # django-ckeditor默认使用default配置

    'default': {

        # 编辑器宽度自适应
        'width': 'auto',
        'height': '300px',
        # tab键转换空格数
        'tabSpaces': 4,
        # 工具栏风格
        'toolbar': 'Custom',
        # 工具栏按钮
        'toolbar_Custom': [
            ['Source', '-', 'Save', 'NewPage', 'DocProps', 'Preview', 'Print', '-', 'Templates'],
            # 格式、字体、大小
            ['Format', 'Font', 'FontSize'],
            # 字体风格
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
            ['Find', 'Replace', '-', 'SelectAll', '-', 'SpellChecker', 'Scayt'],
            # 字体颜色
            ['TextColor', 'BGColor'],

            # 列表
            ['Image', 'Table', 'NumberedList', 'BulletedList', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak',
             'Iframe'],
            ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],
            # 链接
            ['Link', 'Unlink', 'Anchor'],
            # 预览、表情

            ['Preview', 'Smiley'],
            # 居左，居中，居右
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            # 最大化
            ['Maximize'],
            # ['CodeSnippet', 'Markdown'],  # 这个markdown插件默认没有，得额外下载。
        ],
        # 加入代码块插件
        'extraPlugins': ','.join(['codesnippet', 'image2', 'filebrowser', 'widget', 'lineutils']),  # 'markdown'
    },

    # 评论

    'comment': {

        # 编辑器宽度自适应
        'width': 'auto',
        'height': '140px',
        # tab键转换空格数
        'tabSpaces': 4,
        # 工具栏风格
        'toolbar': 'Custom',
        # 工具栏按钮
        'toolbar_Custom': [
            # 表情 代码块
            ['Smiley', 'CodeSnippet'],
            # 字体风格
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
            # 字体颜色
            ['TextColor', 'BGColor'],
            # 链接
            ['Link', 'Unlink'],
            # 列表
            ['NumberedList', 'BulletedList'],
        ],
        # 加入代码块插件
        'extraPlugins': ','.join(['codesnippet']),

    }

}
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

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


# MIDDLEWARE_CLASSES = (
#
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware', # 注意顺序
#
# )
# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     '*'
# 'http://127.0.0.1:8080'
# )

# 异步支持,爬取数据时处理
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

ALLOWED_HOSTS = ['*']
CORS_ALLOWED_ORIGINS_REGEXES = [
    r'^https://.*?$',
]
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

# 当然使用SimpleUI系统菜单也有优点，比如用户拥有什么模型的权限就显示什么菜单。自定义menus中输出的菜单不会受权限控制。如果你想要在后台使用基于RBAC控制的菜单，就不要通过SIMPLEUI_CONFIG自定义菜单
#
SIMPLEUI_CONFIG = {
    # 是否使用系统默认菜单，自定义菜单时建议关闭。
    'system_keep': False,

    # # 用于菜单排序和过滤, 不填此字段为默认排序和全部显示。空列表[] 为全部不显示.
    # 'menu_display': ['后台组织管理', '前台用户管理', '黑土管理', '数据管理', '地图管理', 'Igais管理',
    #                  '文档管理', '爬取数据管理', 'WDC-RRE', '专题资源管理', '翻译库管理', '地名库管理','长春工程管理','中南专栏'],

    # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时刷新展示菜单内容。
    # 一般建议关闭。
    'dynamic': True,
    'menus': [
        {
            'app': 'users',
            'name': '后台组织管理',
            'icon': 'fas fa-user-shield',
            'models': [
                {
                    'name': '角色管理',
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
            'name': '数据管理',
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
                    'name': '文献作者',
                    'url': '/admin/literature_author/literatureauthor/',
                    'icon': 'fa fa-tasks'
                },
                {
                    'name': '文献日期',
                    'url': '/admin/literature_date/literaturedate/',
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

            ]
        },

        {
            'app': 'changchun_project',
            'name': '长春工程管理',
            'icon': 'fa fa-th-list',
            'models': [
                {
                    'name': '长春工程管理',
                    'icon': 'fa fa-th-list',
                    'url': '/admin/changchun_project/changchunproject/'
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
}