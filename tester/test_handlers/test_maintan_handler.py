# -*- coding:utf-8 -*-
'''
Test
'''
from torcms.handlers.category_maintain_handler import MaintainCategoryAjaxHandler, MaintainCategoryHandler


def test_vz():
    '''
    Test
    '''
    urls = [
        ("/label/(.*)", MaintainCategoryAjaxHandler, dict()),
        ("/label/(.*)", MaintainCategoryHandler, dict()),
    ]

    assert urls
