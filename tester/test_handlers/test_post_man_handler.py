# -*- coding:utf-8 -*-

from torcms.handlers.post_manager import PostManHandler


def Test():
    urls = [
        ("/post_man/(.*)", PostManHandler, dict()),
    ]
    assert urls
