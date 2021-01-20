# -*- coding:utf-8 -*-

'''
Router for extor.
'''
from torcms.handlers.post_handler import PostHandler
from torcms.handlers.referrer_handler import Referrer

urls = [
    # ("/subsite/(.*)", tornado.web.StaticFileHandler, {"path": '/home/bk/coding/ResForm/template/static_pages'}),
    ('/special/(.*)', PostHandler, dict(kind='s', filter_view=True)),
    ('/referrer/(.*)', Referrer, dict(kind='r')),
]  # type: List[int]
