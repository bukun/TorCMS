# -*- coding:utf-8 -*-

from torcms.handlers.category_handler import CategoryHandler, MCategory


def Test():
    urls = [
        ("/label/(.*)", CategoryHandler, dict()),
        ("/label/(.*)", MCategory, dict()),
    ]

    assert urls
