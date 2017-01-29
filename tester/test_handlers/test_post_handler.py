# -*- coding:utf-8 -*-


from tornado.testing import AsyncHTTPSTestCase, gen_test

from application import  app



class TestSomeHandler(AsyncHTTPSTestCase):
    def get_app(self):
        return app

    def test_to_add(self):
        response = self.fetch('/post/_add')
        self.assertEqual(response.code, 200)


    def test_index(self):
        response = self.fetch('/post/')
        # response = self.http_client.fetch('/post/_add')
        self.assertEqual(response.code, 200)