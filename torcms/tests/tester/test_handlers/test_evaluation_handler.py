# -*- coding:utf-8 -*-
'''
EvaluationHandler
'''


import sys

sys.path.append('')

from tornado.testing import AsyncHTTPSTestCase

from server import APP


class TestSomeHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_index(self):
        '''
        Test index.
        '''
        response = self.fetch('/evaluate/')
        self.assertEqual(response.code, 200)
