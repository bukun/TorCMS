# -*- coding:utf-8 -*-

'''
ListHandler
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

    def test_list(self):
        '''
        Test index.
        '''
        response = self.fetch('/list/')
        self.assertEqual(response.code, 200)
