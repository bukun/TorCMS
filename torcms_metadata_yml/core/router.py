# -*- coding:utf-8 -*-


from torcms_metadata_yml.handlers.meta_handler import MetadataHandler

_urls = [
    ("/datayml/(.*)", MetadataHandler, dict(kind='7')),

]
