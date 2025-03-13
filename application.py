"""
The Application.
"""


from pathlib import Path
import router as app_router
import torcms.core.router
import torcms.core.uifunction as uifuncs
from config import ADDONS, SITE_CFG, config_modules
from torcms.modules.modef import core_modules

# 注册各个应用的模块，路由
APP_MODUES = dict(core_modules, **config_modules)
APP_URLS = app_router.urls + torcms.core.router.urls

for addon in ADDONS:
    _imp_mod = __import__(f"{addon}.modules.modef")
    _imp_router = __import__(f"{addon}.core.router")
    APP_MODUES = dict(APP_MODUES, **_imp_mod.modules.modef._modules)
    APP_URLS = APP_URLS + _imp_router.core.router._urls

SETTINGS = {
    "template_path": Path("templates"),
    "static_path": Path("static"),
    "debug": SITE_CFG["DEBUG"],
    "cookie_secret": SITE_CFG["cookie_secret"],
    "login_url": "/user/login",
    "ui_modules": APP_MODUES,
    "ui_methods": uifuncs,
}

# CACHES_PATH = os.path.join(os.path.dirname(__file__), "templates", 'caches')
# if os.path.exists(CACHES_PATH):
#     pass
# else:
#     os.mkdir(CACHES_PATH)
