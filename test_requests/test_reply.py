import json
import os
import unittest

import requests
from tornado.testing import AsyncHTTPTestCase

from cfg import SITE_CFG
from server import APP
from torcms.model.reply_model import MReply

reply_list = MReply.query_all()

domain = SITE_CFG['site_url']



class TestTornado(AsyncHTTPTestCase):
    def get_app(self):
        return APP


    def test_reply_list(self):
        for reply in reply_list:
            response = requests.get(os.path.join(domain,'reply/more/{0}'.format(reply)))

            self.assertEqual(response.status_code, 200)

