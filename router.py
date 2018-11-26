# -*- coding:utf-8 -*-

'''
Router for extor.
'''
from torcms.handlers.post_handler import PostHandler
from extor.handler.ext_excel import ExtExcelHandler
import tornado.web



urls = [
    # ("/subsite/(.*)", tornado.web.StaticFileHandler, {"path": '/home/bk/coding/ResForm/template/static_pages'}),
    ('/special/(.*)', PostHandler, dict(kind='s', filter_view=True)),
    ('/ext_excel/(.*)', ExtExcelHandler, dict()),
] # type: List[int]
