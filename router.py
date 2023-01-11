# -*- coding:utf-8 -*-

'''
Router for extor.
'''
from torcms.handlers.referrer_handler import Referrer
from torcms.handlers.post_handler import PostHandler

urls = [
    ("/question/(.*)", PostHandler, dict(kind='q')),
    ('/referrer/(.*)', Referrer, dict(kind='r')),
]  # type: List[int]
