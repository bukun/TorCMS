# -*- coding:utf-8 -*-

from torcms.handlers.post_history_handler import PostHistoryHandler


def Test():
    urls = [
        ("/post_man/(.*)", PostHistoryHandler, dict()),
    ]
    assert urls
