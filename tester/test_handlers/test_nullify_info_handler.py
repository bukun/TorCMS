# -*- coding:utf-8 -*-

'''
NullifyinfoHandler
'''
import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from application import APP


class TestNullifyinfoHandler(AsyncHTTPSTestCase):
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
        response = self.fetch('/nullify_info/')
        self.assertEqual(response.code, 200)

    def test_index_sec(self):
        '''
        Test index.
        '''
        response = self.fetch('/nullify_info/list')
        self.assertEqual(response.code, 200)

    def test_index_cur(self):
        '''
        Test index.
        '''
        response = self.fetch('/nullify_info/list/2')
        self.assertEqual(response.code, 200)
