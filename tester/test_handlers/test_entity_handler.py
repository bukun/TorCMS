# -*- coding:utf-8 -*-

from torcms.handlers.entity_handler import EntityHandler


def Test():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", EntityHandler, dict()), ]
    assert urls
