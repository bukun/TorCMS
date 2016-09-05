# -*- coding:utf-8 -*-

from torcms.handlers.info2reply_handler import Info2ReplyHandler


def Test():
    urls = [
        ("/label/(.*)", Info2ReplyHandler, dict()),
    ]

    assert urls
