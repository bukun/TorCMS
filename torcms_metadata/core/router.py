# -*- coding:utf-8 -*-

from torcms_metadata.handlers.meta_handler import MetadataHandler
_urls = [

    ("/data/(.*)", MetadataHandler, dict(kind='9'))
]
