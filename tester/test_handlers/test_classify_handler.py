# -*- coding:utf-8 -*-

'''
ClassifyHandler
'''
import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from application import APP


class TestClassifyHandler(AsyncHTTPSTestCase):
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
        response = self.fetch('/classify/')
        self.assertEqual(response.code, 200)

    def test_index_sec(self):
        '''
        Test index.
        '''
        response = self.fetch('/classify/list')
        self.assertEqual(response.code, 200)

    def test_index_cur(self):
        '''
        Test index.
        '''
        response = self.fetch('/classify/list/2')
        self.assertEqual(response.code, 200)