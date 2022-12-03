# -*- coding:utf-8 -*-
from torcms_app.handlers.app_handler import YuansuanHandler
from torcms_app.handlers.app_calcinfo_handler import CalcInfo

_urls = [
    ('/app/(.*)', YuansuanHandler, dict(kind='s')),
    ('/calcinfo/(.*)', CalcInfo, dict()),
]
