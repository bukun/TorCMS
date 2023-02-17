# -*- coding:utf-8 -*-

from extor.handlers.meta_ext_handler import MetaExtHander
_urls = [

    ("/data/(.*)", MetaExtHander, dict(kind='9'))
]
