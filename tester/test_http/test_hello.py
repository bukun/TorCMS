'''
运行单元测试时，服务器可以关闭开启，不影响
'''
import unittest

from tornado.testing import AsyncHTTPClient, AsyncHTTPTestCase

# from server import application
from application import APP as application


class TestMain(AsyncHTTPTestCase):
    def get_app(self):
        return application

    def test_main(self):
        response = self.fetch('/')
        print(response.body)
        self.assertEqual(response.code, 200)
        # self.assertEqual(response.body, b'Hello, world')

    def test_hello(self):
        client = AsyncHTTPClient()
