# -*- coding:utf-8 -*-

'''
Test Post handler
'''


from tornado.testing import AsyncHTTPSTestCase
from application import APP


class TestPostHandler(AsyncHTTPSTestCase):
    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_to_add(self):
        '''
        Test
        '''
        response = self.fetch('/post/_add')
        self.assertEqual(response.code, 200)

    def test_index(self):
        '''
        Test
        '''
        response = self.fetch('/post/')
        # response = self.http_client.fetch('/post/_add')
        self.assertEqual(response.code, 200)
