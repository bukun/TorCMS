# -*- coding:utf-8 -*-

from torcms.handlers.meta_handler import MetaHandler


def Test():
    urls = [
        ("/label/(.*)", MetaHandler, dict()),
    ]

    assert urls
