# coding:utf-8

'''
The Application.
'''

import os
import tornado.web
import torcms.core.uifunction as uifuncs
from config import SITE_CFG

from modules import _CUR_MODUES
from urls import _urls


SETTINGS = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    'debug': SITE_CFG['DEBUG'],
    "cookie_secret": SITE_CFG['cookie_secret'],
    "login_url": "/user/login",
    'ui_modules': _CUR_MODUES,
    'ui_methods': uifuncs
}

APP = tornado.web.Application(
    handlers=_urls,
    **SETTINGS
)
