# -*- coding:utf-8 -*-

'''
Test user handler
'''

from tornado.testing import AsyncHTTPSTestCase, gen_test

from application import app


class TestSearchHandler(AsyncHTTPSTestCase):
    def get_app(self):
        return app

    def test_to_add(self):
        response = self.fetch('/search/')
        self.assertEqual(response.code, 200)
