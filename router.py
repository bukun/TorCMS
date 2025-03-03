# -*- coding:utf-8 -*-

'''
Router for extor.
'''
from torcms.handlers.post_handler import PostHandler
from torcms.handlers.referrer_handler import Referrer

# from torcms.handlers.static_handler import StaticHandler
urls = [
    ("/topic/(.*)", PostHandler, dict(kind='q')),
    ('/referrer/(.*)', Referrer, dict(kind='r')),
    # ('/map-show/(.*)', PostHandler, dict(kind='v')),
    ("/tutorial/(.*)", PostHandler, dict(kind='k')),
    # ("/(.*)", StaticHandler, dict()),
]  # type: List[int]
