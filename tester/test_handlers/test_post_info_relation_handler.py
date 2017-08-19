# -*- coding:utf-8 -*-

from torcms.handlers.relation_handler import RelHandler

def Test():
    # assert InfoHandler(dict(), request="/entity/(.*)")
    urls = [
        ("/label/(.*)", RelHandler, dict()), ]
    assert urls
