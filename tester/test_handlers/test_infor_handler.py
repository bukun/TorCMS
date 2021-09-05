# -*- coding:utf-8 -*-
'''
Test
'''
from torcms.handlers.post_handler import PostHandler


def test_ab():
    '''
    Test
    '''
    # assert InfoHandler({}, request="/entity/(.*)")
    urls = [
        ("/label/(.*)", PostHandler, {}), ]
    assert urls
