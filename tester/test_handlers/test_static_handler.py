# -*- coding:utf-8 -*-

from torcms.handlers.static_handler import StaticHandler


def Test():
    urls = [
        ("/label/(.*)", StaticHandler, dict()),
    ]
    assert urls
