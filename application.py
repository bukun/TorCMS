# coding:utf-8

'''
The Application.
'''

import os
from config import SITE_CFG
from urls import urls
import tornado.web

from torcms.modules.modef import core_modules
import torcms.core.uifunction as uifuncs

CUR_MODUES = {}  # type: Dict[str, object]

SETTINGS = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    'debug': SITE_CFG['DEBUG'],
    "cookie_secret": SITE_CFG['cookie_secret'],
    "login_url": "/user/login",
    'ui_modules': dict(core_modules, **CUR_MODUES),
    'ui_methods': uifuncs
}

APP = tornado.web.Application(
    handlers=urls,
    **SETTINGS
)
