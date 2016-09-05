# -*- coding:utf-8 -*-

from torcms.handlers.info_handler import InfoHandler


def Test():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", InfoHandler, dict()), ]
    assert urls
