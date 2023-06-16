# -*- coding:utf-8 -*-
'''
PostHandler kind=3
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

    def test_info(self):
        '''
        Test info.
        '''
        response = self.fetch('/info/')
        self.assertEqual(response.code, 200)

    def test_to_add(self):
        '''
        Test add.
        '''
        response = self.fetch('/info/_add/')
        self.assertEqual(response.code, 200)

    def test_to_edit(self):
        '''
        Test edit.
        '''
        response = self.fetch('/info/_edit/')
        self.assertEqual(response.code, 200)
    def test_to_delete(self):
        '''
        Test delete.
        '''
        response = self.fetch('/info/_delete/')
        self.assertEqual(response.code, 200)

    def test_to_cat_add(self):
        '''
        Test cat_add.
        '''
        response = self.fetch('/info/_cat_add/')
        self.assertEqual(response.code, 200)

    def test_to_index(self):
        '''
        Test index.
        '''
        response = self.fetch('/info/index')
        self.assertEqual(response.code, 200)