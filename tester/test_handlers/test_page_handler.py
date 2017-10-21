# -*- coding:utf-8 -*-

'''
Test Post handler
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
        # response = self.http_client.fetch('/post/_add')
        self.assertEqual(response.code, 400)
