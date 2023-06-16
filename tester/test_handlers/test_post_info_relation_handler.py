# -*- coding:utf-8 -*-
'''
Test
'''

from tornado.testing import AsyncHTTPSTestCase

from application import APP


class TestPostHandler(AsyncHTTPSTestCase):
    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_Rel(self):
        '''
        Test post.
        '''
        response = self.fetch('/rel/1/')
        self.assertEqual(response.code, 200)

