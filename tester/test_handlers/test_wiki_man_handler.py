# -*- coding:utf-8 -*-

from torcms.handlers.wiki_manager import WikiManHandler


def Test():
    urls = [
        ("/wiki_man/(.*)", WikiManHandler, dict()),
    ]
    assert urls
