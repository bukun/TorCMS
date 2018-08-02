# -*- coding:utf-8 -*-

'''
Test
'''
from torcms.handlers.list_handler import ListHandler, MCategory


def Test():
    '''
    Test
    '''
    urls = [
        ("/label/(.*)", ListHandler, dict()),
        ("/label/(.*)", MCategory, dict()),
    ]

    assert urls
