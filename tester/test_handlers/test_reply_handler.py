# -*- coding:utf-8 -*-
'''
Test
'''
from torcms.handlers.reply_handler import ReplyHandler


def test_b():
    urls = [
        ("/label/(.*)", ReplyHandler, dict()),
    ]
    assert urls
