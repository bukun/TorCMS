# # -*- coding:utf-8 -*-
#
from torcms.handlers.label_handler import InfoTagHandler


def Test():
    urls = [
        ("/label/(.*)", InfoTagHandler, {}),
    ]

    assert urls is not None
