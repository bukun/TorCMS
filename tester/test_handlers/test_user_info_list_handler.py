# -*- coding:utf-8 -*-
'''
Test
'''
from torcms.handlers.user_info_list_handler import UserListHandler


def test_a():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", UserListHandler, dict()),
    ]
    assert urls
