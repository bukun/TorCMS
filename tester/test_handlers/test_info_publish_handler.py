# -*- coding:utf-8 -*-

from torcms.handlers.publish_handler import PublishHandler


def Test():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", PublishHandler, dict()), ]
    assert urls

