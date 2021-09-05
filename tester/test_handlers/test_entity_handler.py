# -*- coding:utf-8 -*-

'''
Test
'''
from torcms.handlers.entity_handler import EntityHandler


def Test():
    '''
    Test
    '''
    # assert InfoHandler({}, request="/entity/(.*)")
    urls = [
        ("/label/(.*)", EntityHandler, {}), ]
    assert urls
