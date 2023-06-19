# -*- coding:utf-8 -*-

'''
CatalogHandler
'''
import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from application import APP


class TestCatalogHandler(AsyncHTTPSTestCase):
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
        response = self.fetch('/catalog/')
        self.assertEqual(response.code, 200)

