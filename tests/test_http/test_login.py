import json
import unittest

from tornado.testing import AsyncHTTPTestCase

from server import APP


class TestTornado(AsyncHTTPTestCase):
    def get_app(self):
        return APP

    def test_BaseHandler(self):
        # 测试正常输入文本
        # data = json.dumps({"text": ""})
        # data = {"user_name": "bukun"}

        # response = self.fetch("/user/login",method="POST",body=data)
        response = self.fetch("/user/login")
        # self.assertEqual(eval(response.body)["data"], "test")
        self.assertEqual(response.code, 200)

