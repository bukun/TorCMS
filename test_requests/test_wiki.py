import json
import os
import unittest

import requests
from tornado.testing import AsyncHTTPTestCase

from cfg import SITE_CFG
from server import APP
from torcms.model.wiki_model import MWiki

domain = SITE_CFG['site_url']


wiki_list = MWiki.query_all(limit=None)

class TestTornado(AsyncHTTPTestCase):
    def get_app(self):
        return APP


    def test_wiki_list(self):
        for wiki in wiki_list:
            response = requests.get(os.path.join(domain,'wiki/{0}'.format(wiki)))

            self.assertEqual(response.status_code, 200)

