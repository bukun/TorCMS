# -*- coding:utf-8 -*-
'''
Test
'''
from torcms.handlers.relation_handler import RelHandler


def test_lz():
    # assert InfoHandler({}, request="/entity/(.*)")
    urls = [
        ("/label/(.*)", RelHandler, {}), ]
    assert urls
