import json
import os
import unittest

import requests
from cfg import SITE_CFG
from tornado.testing import AsyncHTTPTestCase

from server import APP

domain = SITE_CFG['site_url']


class TestTornado(AsyncHTTPTestCase):
    def get_app(self):
        return APP

    def test_BaseHandler(self):
        # 测试正常输入文本

        data = {"user_name": "bukun"}

        response = requests.post(os.path.join(domain, "user/login"), json=data)
        # self.assertEqual(eval(response.body)["data"], "test")
        self.assertEqual(response.status_code, 500)
