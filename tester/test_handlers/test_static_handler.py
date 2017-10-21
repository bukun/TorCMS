# -*- coding:utf-8 -*-

'''
Test
'''
from torcms.handlers.static_handler import StaticHandler


def test_zl():
    '''
    Test
    '''
    urls = [
        ("/label/(.*)", StaticHandler, dict()),
    ]
    assert urls
