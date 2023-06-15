# -*- coding:utf-8 -*-
'''
PostHandler kind=3
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

    def test_info(self):
        '''
        Test info.
        '''
        response = self.fetch('/info/')
        self.assertEqual(response.code, 200)

