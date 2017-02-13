# -*- coding:utf-8 -*-

# -*- coding:utf-8 -*-

'''
Test Post handler
'''

from tornado.testing import AsyncHTTPSTestCase, gen_test

from application import app


class TestWikiHandler(AsyncHTTPSTestCase):
    def get_app(self):
        return app

    def test_to_add(self):
        response = self.fetch('/wiki/ToAdd')
        # Not log in.
        self.assertEqual(response.code, 500)

    def test_index(self):
        response = self.fetch('/post/')
        # response = self.http_client.fetch('/post/_add')
        self.assertEqual(response.code, 200)
