# -*- coding:utf-8 -*-

'''
Router for extor.
'''
from torcms.handlers.post_handler import PostHandler
from torcms.handlers.referrer_handler import Referrer

urls = [

    ('/referrer/(.*)', Referrer, dict(kind='r')),
]  # type: List[int]
