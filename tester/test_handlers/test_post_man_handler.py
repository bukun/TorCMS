# -*- coding:utf-8 -*-
'''
Test
'''
from torcms.handlers.post_history_handler import PostHistoryHandler


def test_k():
    '''
    Test
    '''
    urls = [
        ("/post_man/(.*)", PostHistoryHandler, dict()),
    ]
    assert urls
