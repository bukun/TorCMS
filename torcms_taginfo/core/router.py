# -*- coding:utf-8 -*-
from torcms_taginfo.handlers.datalist_handler import DatalistHandler
from torcms_taginfo.handlers.export_data_handler import DownloadDataHandler
from torcms_taginfo.handlers.update_category_handler import UpdateCategoryHandler

_urls = [
    ("/dataset/(.*)", DatalistHandler),
    ("/download/(.*)", DownloadDataHandler),
    ("/update_category/(.*)", UpdateCategoryHandler)
]
