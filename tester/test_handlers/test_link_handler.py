# -*- coding:utf-8 -*-

'''
LinkHandler LinkPartialHandler
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

    def test_link(self):
        '''
        Test index.
        '''
        response = self.fetch('/link/')
        self.assertEqual(response.code, 200)
    def test_link_j(self):
        '''
        Test index.
        '''
        response = self.fetch('/link_j/')
        self.assertEqual(response.code, 200)