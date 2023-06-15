# -*- coding:utf-8 -*-

'''
LogHandler
'''

import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from application import APP


class TestSomeHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_log(self):
        '''
        Test index.
        '''
        response = self.fetch('/log/')
        self.assertEqual(response.code, 200)
    def test_log_j(self):
        '''
        Test index.
        '''
        response = self.fetch('/log_j/')
        self.assertEqual(response.code, 200)