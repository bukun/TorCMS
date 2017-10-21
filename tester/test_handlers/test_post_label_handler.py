# -*- coding:utf-8 -*-
'''
Test
'''
from torcms.handlers.label_handler import LabelHandler


def test_bb():
    '''
    Test
    '''
    urls = [
        ("/label/(.*)", LabelHandler, dict()),
    ]

    assert urls
