# -*- coding:utf-8 -*-

from torcms.handlers.info_category_hanlder import InforCategoryHandler


def Test():
    urls = [
        ("/label/(.*)", InforCategoryHandler, dict()),
    ]

    assert urls
