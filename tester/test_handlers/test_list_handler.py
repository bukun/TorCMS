# -*- coding:utf-8 -*-

'''
ListHandler
'''
import sys

sys.path.append('.')

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

    def test_list(self):
        '''
        Test index.
        '''
        response = self.fetch('/list/')
        self.assertEqual(response.code, 200)

    def test_to_j_subcat(self):
        '''
        Test j_subcat.
        '''
        response = self.fetch('/list/j_subcat')
        self.assertEqual(response.code, 200)

    def test_to_j_kindcat(self):
        '''
        Test j_kindcat.
        '''
        response = self.fetch('/list/j_kindcat')
        self.assertEqual(response.code, 200)

    def test_to_j_list_catalog(self):
        '''
        Test j_list_catalog.
        '''
        response = self.fetch('/list/j_list_catalog')
        self.assertEqual(response.code, 200)
