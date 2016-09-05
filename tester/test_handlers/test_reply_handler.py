# -*- coding:utf-8 -*-

from torcms.handlers.reply_handler import ReplyHandler


def Test():
    urls = [
        ("/label/(.*)", ReplyHandler, dict()),
    ]
    assert urls
