# -*- coding:utf-8 -*-
from torcms_app.handlers.app_calcinfo_handler import CalcInfo
from torcms_app.handlers.app_handler import YuansuanHandler
from torcms_app.handlers.javascript_handler import JavascriptHandler

_urls = [
    ('/app/(.*)', YuansuanHandler, dict(kind='s', cache=False)),
    ('/calcinfo/(.*)', CalcInfo, dict()),
    ('/py/(.*)', JavascriptHandler, dict()),
]
