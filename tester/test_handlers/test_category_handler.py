# -*- coding:utf-8 -*-

'''
Test
'''
from torcms.handlers.category_handler import CategoryHandler, MCategory


def Test():
    '''
    Test
    '''
    urls = [
        ("/label/(.*)", CategoryHandler, dict()),
        ("/label/(.*)", MCategory, dict()),
    ]

    assert urls
