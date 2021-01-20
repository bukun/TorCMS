# -*- coding:utf-8 -*-
'''
Test
'''
from torcms.handlers.relation_handler import RelHandler


def test_lz():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", RelHandler, dict()), ]
    assert urls
