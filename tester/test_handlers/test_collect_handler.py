# -*- coding:utf-8 -*-

'''
Test
'''
from torcms.handlers.collect_handler import CollectHandler


def Test():
    '''
    Test
    '''
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", CollectHandler, dict()), ]
    assert urls
