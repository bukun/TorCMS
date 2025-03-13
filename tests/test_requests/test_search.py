import json
import os
import unittest

from faker import Faker

fak = Faker('zh_CN')

import requests
from tornado.testing import AsyncHTTPTestCase

from cfg import SITE_CFG
from server import APP
from torcms.model.wiki_model import MWiki

domain = SITE_CFG['site_url']


class TestTornado(AsyncHTTPTestCase):
    def get_app(self):
        return APP

    def test_wiki_list(self):
        for ii in range(20):
            tt = fak.text()[10]
            response = requests.get(os.path.join(domain, f'search/{tt}/{ii}'))
            self.assertEqual(response.status_code, 200)
