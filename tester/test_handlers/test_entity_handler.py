# -*- coding:utf-8 -*-

'''
EntityHandler
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

    def test_index(self):
        '''
        Test index.
        '''
        response = self.fetch('/entity/')
        self.assertEqual(response.code, 200)
    def test_to_add(self):
        '''
        Test add.
        '''
        response = self.fetch('/entity/_add')
        self.assertEqual(response.code, 200)
    def test_to_list(self):
        '''
        Test list.
        '''
        response = self.fetch('/entity/list')
        self.assertEqual(response.code, 200)