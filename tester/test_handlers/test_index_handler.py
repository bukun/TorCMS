# -*- coding:utf-8 -*-


from tornado.testing import AsyncHTTPSTestCase

from application import app


class TestSomeHandler(AsyncHTTPSTestCase):
    def get_app(self):
        return app

    def test_index(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
