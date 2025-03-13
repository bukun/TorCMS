import json
import unittest

from tornado.testing import AsyncHTTPTestCase

from server import APP

from torcms.model.wiki_model import MWiki

wiki_list = MWiki.query_all(limit=None)


class TestTornado(AsyncHTTPTestCase):
    def get_app(self):
        return APP


    def test_wiki_list(self):
        for wiki in wiki_list:

            response = self.fetch('/wiki/{0}'.format(wiki))
            self.assertEqual(response.code, 200)
    def test_page(self):
        for wiki in wiki_list:

            response = self.fetch('/page/{0}'.format(wiki))
            self.assertEqual(response.code, 200)
