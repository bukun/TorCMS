# -*- coding:utf-8 -*-

from torcms.handlers.wiki_handler import WikiHandler


def Test():
    urls = [
        ("/label/(.*)", WikiHandler, dict()),
    ]
    assert urls
