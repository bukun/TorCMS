# -*- coding:utf-8 -*-

'''
Test
'''
from torcms.handlers.admin_handler import AdminHandler


def Test():
    '''
    Test
    '''
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [("/label/(.*)", AdminHandler, dict()), ]
    assert urls
