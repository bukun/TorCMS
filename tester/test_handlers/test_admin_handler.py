# -*- coding:utf-8 -*-

'''
Test
'''
import sys

sys.path.append('.')
from torcms.handlers.admin_handler import AdminHandler


def Test():
    '''
    Test
    '''
    # assert InfoHandler({}, request="/entity/(.*)")
    urls = [("/label/(.*)", AdminHandler, {}), ]
    assert urls
