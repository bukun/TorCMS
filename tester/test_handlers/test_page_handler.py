# -*- coding:utf-8 -*-

from torcms.handlers.page_handler import PageHandler
from torcms.handlers.page_ajax_handler import PageAjaxHandler


def Test():
    urls = [
        ("/label/(.*)", PageAjaxHandler, dict()),
        ("/label/(.*)", PageHandler, dict()),
    ]
    assert urls
