# -*- coding:utf-8 -*-


from torcms_metadata.handlers.meta_handler import MetadataHandler

_urls = [
    ("/dde/(.*)", MetadataHandler, dict(kind='d',  filter_view=True))
]
