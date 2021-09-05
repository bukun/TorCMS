# -*- coding:utf-8 -*-

'''
Test
'''
from torcms.handlers.collect_handler import CollectHandler


def Test():
    '''
    Test
    '''
    # assert InfoHandler({}, request="/entity/(.*)")
    urls = [
        ("/label/(.*)", CollectHandler, {}), ]
    assert urls
