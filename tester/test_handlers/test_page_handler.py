# -*- coding:utf-8 -*-

'''
Test Post handler
'''

from torcms.handlers.post_handler import PostHandler

# from tornado.testing import AsyncHTTPSTestCase
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from application import SETTINGS, app


class TestPageHandler(AsyncHTTPTestCase):
    def get_app(self):
        return app

    def test_to_add(self):
        response = self.fetch('/page/_add')
        self.assertEqual(response.code, 200)

    def test_index(self):
        response = self.fetch('/page/')
        # response = self.http_client.fetch('/post/_add')
        self.assertEqual(response.code, 400)
