# -*- coding:utf-8 -*-

from torcms.handlers.label_handler import LabelHandler


def Test():
    urls = [
        ("/label/(.*)", LabelHandler, dict()),
    ]

    assert urls
