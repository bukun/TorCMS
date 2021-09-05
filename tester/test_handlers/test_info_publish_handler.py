# -*- coding:utf-8 -*-
'''
Test
'''
from torcms.handlers.publish_handler import PublishHandler


def Test():
    '''
    Test
    '''
    # assert InfoHandler({}, request="/entity/(.*)")
    urls = [
        ("/label/(.*)", PublishHandler, {}), ]
    assert urls
