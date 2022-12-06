# -*- coding:utf-8 -*-


from torcms_dde.handlers.meta_handler import MetadataHandler

_urls = [
    ("/dde/(.*)", MetadataHandler, dict(kind='d'))
]
