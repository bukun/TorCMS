# -*- coding:utf-8 -*-
'''
CategoryAjaxHandler
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
        response = self.fetch('/category_j/')
        self.assertEqual(response.code, 200)

    def test_to_add(self):
        '''
        Test add.
        '''
        response = self.fetch('/category_j/_add')
        self.assertEqual(response.code, 200)

    def test_to_list(self):
        '''
        Test list.
        '''
        response = self.fetch('/category_j/list')
        self.assertEqual(response.code, 200)
