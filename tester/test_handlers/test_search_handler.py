# -*- coding:utf-8 -*-

from torcms.handlers.search_handler import SearchHandler


def Test():
    urls = [
        ("/label/(.*)", SearchHandler, dict()),
    ]
    assert urls
