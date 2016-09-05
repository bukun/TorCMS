# -*- coding:utf-8 -*-

from torcms.handlers.page_handler import PageAjaxHandler, PageHandler


def Test():
    urls = [
        ("/label/(.*)", PageAjaxHandler, dict()),
        ("/label/(.*)", PageHandler, dict()),
    ]
    assert urls
