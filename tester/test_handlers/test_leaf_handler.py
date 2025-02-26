# -*- coding:utf-8 -*-

'''
CollectHandler
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

    def test_add(self):
        '''
        Test add.
        '''
        response = self.fetch('/leaf/_add/')
        self.assertEqual(response.code, 200)

    def test_edit_kind(self):
        '''
        Test edit_kind.
        '''
        response = self.fetch('/leaf/_edit_kind/')
        self.assertEqual(response.code, 200)

    def test_edit(self):
        '''
        Test edit.
        '''
        response = self.fetch('/leaf/_edit/')
        self.assertEqual(response.code, 200)

    def test_cat_add(self):
        '''
        Test cat_add.
        '''
        response = self.fetch('/leaf/_cat_add/')
        self.assertEqual(response.code, 200)
