# -*- coding:utf-8 -*-
'''
Test
'''
from torcms.handlers.category_handler import CategoryAjaxHandler


def test_vz():
    '''
    Test
    '''
    urls = [
        ("/label/(.*)", CategoryAjaxHandler, dict()),

    ]

    assert urls
