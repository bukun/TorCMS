# -*- coding:utf-8 -*-

from torcms.handlers.post_info_relation_handler import RelHandler

def Test():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", RelHandler, dict()), ]
    assert urls
