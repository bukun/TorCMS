# -*- coding:utf-8 -*-


from tornado.testing import AsyncHTTPSTestCase

from application import app


class TestSomeHandler(AsyncHTTPSTestCase):
    def get_app(self):
        return app

    def test_index(self):
        response = self.fetch('/')
        # response = self.http_client.fetch('/post/_add')
        self.assertEqual(response.code, 200)
