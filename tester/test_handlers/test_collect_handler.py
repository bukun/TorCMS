# -*- coding:utf-8 -*-

'''
CollectHandler
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
        response = self.fetch('/collect/')
        self.assertEqual(response.code, 200)

    def test_collect_list(self):
        '''
        Test list.
        '''
        response = self.fetch('/collect/list')
        self.assertEqual(response.code, 200)
    def test_collect_remove(self):
        '''
        Test remove.
        '''
        response = self.fetch('/collect/remove')
        self.assertEqual(response.code, 200)