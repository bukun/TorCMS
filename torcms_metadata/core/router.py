# -*- coding:utf-8 -*-


from torcms_metadata.handlers.meta_handler import MetadataHandler
# from torcms_metadata.handlers.meta_filter_handler import MetaFilterHandler

_urls = [
    ("/meta_info/(.*)", MetadataHandler, dict(kind='9')),
    # ("/meta_info_filter/(.*)", MetaFilterHandler, dict(kind='9')),
]
