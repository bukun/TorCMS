# -*- coding:utf-8 -*-
'''
Test
'''
from torcms.handlers.evaluation_handler import EvaluationHandler


def Test():
    '''
    Test
    '''
    # assert InfoHandler({}, request="/entity/(.*)")
    urls = [
        ("/label/(.*)", EvaluationHandler, {}), ]
    assert urls
