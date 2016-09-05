# -*- coding:utf-8 -*-

from torcms.handlers.infolabel_hander import InfoLabelHandler


def Test():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", InfoLabelHandler, dict()), ]
    assert urls
