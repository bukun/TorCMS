# -*- coding:utf-8 -*-

'''
Router for extor.
'''
from torcms.handlers.referrer_handler import Referrer
from torcms.handlers.post_handler import PostHandler
urls = [
    ("/topic/(.*)", PostHandler, dict(kind='q')),
    ('/referrer/(.*)', Referrer, dict(kind='r')),
    # ('/map-show/(.*)', PostHandler, dict(kind='v')),
    ("/tutorial/(.*)", PostHandler, dict(kind='k')),
]  # type: List[int]
