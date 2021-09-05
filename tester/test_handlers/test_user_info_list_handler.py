# -*- coding:utf-8 -*-
'''
Test
'''
from torcms.handlers.user_info_list_handler import UserListHandler


def test_a():
    # assert InfoHandler({}, request="/entity/(.*)")
    urls = [
        ("/label/(.*)", UserListHandler, {}),
    ]
    assert urls
