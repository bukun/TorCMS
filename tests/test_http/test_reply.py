import json
import unittest

from tornado.testing import AsyncHTTPTestCase

from server import APP

from torcms.model.reply_model import MReply

reply_list = MReply.query_all()


class TestTornado(AsyncHTTPTestCase):
    def get_app(self):
        return APP

    def test_reply_list(self):
        for reply in reply_list:
            response = self.fetch('/reply/more/{0}'.format(reply))
            self.assertEqual(response.code, 200)
