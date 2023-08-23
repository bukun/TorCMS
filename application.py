# coding:utf-8

"""
The Application.
"""

import os
from pathlib import Path
import tornado.web
import torcms.core.uifunction as uifuncs
from torcms.modules.modef import core_modules
import router
import torcms.core.router
from config import config_modules
from config import SITE_CFG

# 注册各个应用的模块
CUR_MODUES = dict(core_modules, **config_modules)  # type: Dict[str, object]

for wdir in Path(".").iterdir():
    if wdir.is_dir() and wdir.name.startswith("torcms_"):
        the_file = wdir / 'modules/modef.py'
        if the_file.exists():
            pass
        else:
            continue
        the_mod = f"{wdir.name}.modules.modef"
        _mod = __import__(the_mod)
        CUR_MODUES = dict(CUR_MODUES, **_mod.modules.modef._modules)

# 注册路由
urls = router.urls + torcms.core.router.urls
for wdir in Path(".").iterdir():
    if wdir.is_dir() and wdir.name.startswith("torcms_"):
        the_file = wdir / 'core/router.py'
        if the_file.exists():
            pass
        else:
            continue
        the_mod = f"{wdir.name}.core.router"
        _mod = __import__(the_mod)
        urls = urls + _mod.core.router._urls


SETTINGS = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": SITE_CFG["DEBUG"],
    "cookie_secret": SITE_CFG["cookie_secret"],
    "login_url": "/user/login",
    "ui_modules": CUR_MODUES,
    "ui_methods": uifuncs,
}

APP = tornado.web.Application(handlers=urls, **SETTINGS)
