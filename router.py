# -*- coding:utf-8 -*-

'''
Router for extor.
'''
from torcms.handlers.post_handler import PostHandler
from torcms.handlers.referrer_handler import Referrer
from torcms.handlers.check_handler import CheckHandler
urls = [
    ("/check/(.*)", CheckHandler, dict()),
    ('/referrer/(.*)', Referrer, dict(kind='r')),
]  # type: List[int]
