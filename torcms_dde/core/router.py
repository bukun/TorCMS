# -*- coding:utf-8 -*-


from torcms_dde.handlers.meta_handler import MetadataHandler
from torcms_dde.handlers.json_handler import JsonHandler
from torcms_dde.handlers.search_hander import DirectorySearchHandler

_urls = [
    ("/directory/(.*)", MetadataHandler, dict(kind='d',  filter_view=True)),
    ("/directory_json/(.*)", JsonHandler),
    ("/directory_search/(.*)", DirectorySearchHandler),
]
