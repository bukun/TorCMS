# -*- coding:utf-8 -*-


from torcms_postgis.handlers.meta_handler import MetadataHandler

_urls = [
    ("/postgis/(.*)", MetadataHandler, dict(kind='g')),
]
