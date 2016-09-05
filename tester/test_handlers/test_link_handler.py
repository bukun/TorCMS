# -*- coding:utf-8 -*-

from torcms.handlers.link_handler import LinkHandler


def Test():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", LinkHandler, dict()), ]
    assert urls
