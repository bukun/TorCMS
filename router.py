# -*- coding:utf-8 -*-

'''
Router for extor.
'''
from torcms.handlers.post_handler import PostHandler
urls = [
    ('/special/(.*)', PostHandler, dict(kind='s', filter_view=True)),
] # type: List[int]
