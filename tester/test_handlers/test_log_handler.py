# -*- coding:utf-8 -*-

'''
Test
'''

from torcms.handlers.log_handler import LogHandler, LogPartialHandler


def Test():
    '''
    Test
    '''
    urls = [
        ("/label/(.*)", LogHandler, {}),
        ("/label/(.*)", LogPartialHandler, {}), ]
    assert urls
