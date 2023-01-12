# -*- coding:utf-8 -*-

'''
Router for extor.
'''
from torcms.handlers.referrer_handler import Referrer
from extor.handlers.question_handler import QuestionHandler
urls = [
    ("/question/(.*)", QuestionHandler, dict(kind='q')),
    ('/referrer/(.*)', Referrer, dict(kind='r')),
]  # type: List[int]
