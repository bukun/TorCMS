# -*- coding:utf-8 -*-

'''
Router for extor.
'''
from torcms.handlers.referrer_handler import Referrer
from extor.handlers.topic_handler import TopicHandler
urls = [
    ("/topic/(.*)", TopicHandler, dict(kind='q')),
    ('/referrer/(.*)', Referrer, dict(kind='r')),
]  # type: List[int]
