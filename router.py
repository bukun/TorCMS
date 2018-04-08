# -*- coding:utf-8 -*-

'''
Router for extor.
'''
from torcms.handlers.post_handler import PostHandler
from extor.handler.user2_handler import User2Handler,UserPartialHandler



urls = [
    ('/special/(.*)', PostHandler, dict(kind='s', filter_view=True)),
    ("/user/p/(.*)", UserPartialHandler, dict()),  # Deprecated
    ("/user_p/(.*)", UserPartialHandler, dict()),  # Deprecated
    ("/user_j/(.*)", UserPartialHandler, dict()),
    ("/user/(.*)", User2Handler, dict()),
] # type: List[int]
