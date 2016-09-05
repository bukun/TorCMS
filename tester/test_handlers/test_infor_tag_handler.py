# -*- coding:utf-8 -*-

from torcms.handlers.infor_tag_hanlder import InforTagHandler


def Test():
    urls = [
        ("/label/(.*)", InforTagHandler, dict()),
    ]

    assert urls
