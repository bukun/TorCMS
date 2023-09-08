# -*- coding:utf-8 -*-

'''
Router for extor.
'''
from torcms.handlers.referrer_handler import Referrer
from extor.handlers.topic_handler import TopicHandler
from torcms.handlers.post_handler import PostHandler
from torcms.handlers.leaf_handler import LeafHandler
urls = [
    ("/topic/(.*)", TopicHandler, dict(kind='q')),
    ('/referrer/(.*)', Referrer, dict(kind='r')),
    # ('/map-show/(.*)', PostHandler, dict(kind='v')),
    ("/tutorial/(.*)", LeafHandler, dict(kind='k')),
]  # type: List[int]
