# -*- coding:utf-8 -*-

from torcms.handlers.user_handler import UserHandler, UserAjaxHandler


def Test():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", UserHandler, dict()),
        ("/labelvv/(.*)", UserAjaxHandler, dict()),
    ]
    assert urls
