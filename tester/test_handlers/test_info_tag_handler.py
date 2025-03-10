# # -*- coding:utf-8 -*-
#
from torcms.handlers.label_handler import InfoTagHandler


def test_foo():
    urls = [
        ("/label/(.*)", InfoTagHandler, {}),
    ]

    assert urls is not None
