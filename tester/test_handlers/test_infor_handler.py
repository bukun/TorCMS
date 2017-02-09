# -*- coding:utf-8 -*-

from torcms.handlers.post_handler import PostHandler


def Test():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", PostHandler, dict()), ]
    assert urls
