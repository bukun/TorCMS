# -*- coding:utf-8 -*-


from torcms_dde.handlers.meta_handler import MetadataHandler
from torcms_dde.handlers.json_handler import JsonHandler

_urls = [
    ("/dde/(.*)", MetadataHandler, dict(kind='d',  filter_view=True)),
    ("/json/(.*)", JsonHandler),
]
