# -*- coding:utf-8 -*-

from torcms.handlers.infocate_tag_hanler import InfoTagHandler


def Test():
    urls = [
        ("/label/(.*)", InfoTagHandler, dict()),
    ]

    assert urls
