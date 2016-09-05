# -*- coding:utf-8 -*-

from torcms.handlers.category_handler import CategoryHandler, MPostCatalog


def Test():
    urls = [
        ("/label/(.*)", CategoryHandler, dict()),
        ("/label/(.*)", MPostCatalog, dict()),
    ]

    assert urls
