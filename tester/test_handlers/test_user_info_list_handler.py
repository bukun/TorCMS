# -*- coding:utf-8 -*-

from torcms.handlers.user_info_list_handler import UserListHandler


def Test():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", UserListHandler, dict()),
    ]
    assert urls
