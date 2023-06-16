# -*- coding:utf-8 -*-

'''
Test PageHandler PageAjaxHandler
'''

from tornado.testing import AsyncHTTPTestCase

from application import APP


class TestPageHandler(AsyncHTTPTestCase):
    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_to_add(self):
        '''
        Test
        '''
        response = self.fetch('/page/_add')
        self.assertEqual(response.code, 200)

    def test_index(self):
        '''
        Test
        '''
        response = self.fetch('/page/')
        self.assertEqual(response.code, 400)

    def test_to_edit(self):
        '''
        Test
        '''
        response = self.fetch('/page/_edit/')
        self.assertEqual(response.code, 200)
    def test_to_list(self):
        '''
        Test
        '''
        response = self.fetch('/page/list')
        self.assertEqual(response.code, 200)


class TestPageAjaxHandler(AsyncHTTPTestCase):
    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_to_add(self):
        '''
        Test
        '''
        response = self.fetch('/page_j/_add')
        self.assertEqual(response.code, 200)

    def test_index(self):
        '''
        Test
        '''
        response = self.fetch('/page_j/list/')
        self.assertEqual(response.code, 200)
