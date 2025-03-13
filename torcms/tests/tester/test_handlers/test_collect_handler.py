# -*- coding:utf-8 -*-

'''
CollectHandler
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
        response = self.fetch('/collect/remove/')
        self.assertEqual(response.code, 200)
