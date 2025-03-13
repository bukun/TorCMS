'''
运行单元测试时，服务器可以关闭开启，不影响
'''
import unittest

from tornado.testing import AsyncHTTPClient, AsyncHTTPTestCase

# from server import application
from server import APP


class TestMain(AsyncHTTPTestCase):
    def get_app(self):
        return APP

    def test_main(self):
        response = self.fetch('/')
        print(response.body)
        self.assertEqual(response.code, 200)
        # self.assertEqual(response.body, b'Hello, world')

    def test_hello(self):
        client = AsyncHTTPClient()
