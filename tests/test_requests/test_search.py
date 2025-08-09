import json
import os
import unittest

from faker import Faker

fak = Faker('zh_CN')

import requests
from cfg import SITE_CFG
from tornado.testing import AsyncHTTPTestCase

from server import APP
from torcms.model.wiki_model import MWiki

domain = SITE_CFG['site_url']


class TestTornado(AsyncHTTPTestCase):
    def get_app(self):
        return APP

    def test_wiki_list(self):
        for ii in range(1, 20):
            tt = fak.text()[10]
            the_url = os.path.join(domain, f'search/{tt}/{ii}')
            print('=' * 40)
            print(the_url)
            print('=' * 40)

            response = requests.get(the_url)
            self.assertEqual(response.status_code, 200)
