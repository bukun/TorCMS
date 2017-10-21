# -*- coding:utf-8 -*-
'''
Test
'''
from torcms.handlers.post_handler import PostHandler


def test_ab():
    '''
    Test
    '''
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", PostHandler, dict()), ]
    assert urls
