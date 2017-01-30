# -*- coding:utf-8 -*-

from torcms.handlers.label_hanlder import LabelHandler


def Test():
    urls = [
        ("/label/(.*)", LabelHandler, dict()),
    ]

    assert urls
