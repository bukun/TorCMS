# -*- coding:utf-8 -*-

from torcms.handlers.post_label_handler import PostLabelHandler


def Test():
    urls = [
        ("/label/(.*)", PostLabelHandler, dict()),
    ]

    assert urls
