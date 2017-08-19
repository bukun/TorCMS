# -*- coding:utf-8 -*-

from torcms.handlers.collect_handler import CollectHandler


def Test():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", CollectHandler, dict()), ]
    assert urls
