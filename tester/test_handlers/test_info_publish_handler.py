# -*- coding:utf-8 -*-

from torcms.handlers.infocate_publish_handler import InfoPublishHandler


def Test():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", InfoPublishHandler, dict()), ]
    assert urls

