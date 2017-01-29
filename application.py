# coding:utf-8

import os
import config
from urls import urls
import tornado.web

from torcms.modules.modef import core_modules

cur_modues = {}

modules = dict(core_modules, **cur_modues)

SETTINGS = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    'debug': True,
    "cookie_secret": config.cookie_secret,
    "login_url": "/user/login",
    'ui_modules': modules,
}

app = tornado.web.Application(
    handlers=urls,
    **SETTINGS
)
