import json
import os
import unittest

import requests
from tornado.testing import AsyncHTTPTestCase

from cfg import SITE_CFG
from config import post_cfg
from server import APP
from torcms.model.category_model import MCategory

domain = SITE_CFG['site_url']

tags = MCategory.query_all()


class TestTornado(AsyncHTTPTestCase):
    def get_app(self):
        return APP

    def test_category_label(self):
        for tag in tags:
            if tag.kind in ['1', 'm']:
                response = requests.get(
                    os.path.join(domain, 'list/{0}'.format(tag.slug))
                )

                self.assertEqual(response.status_code, 200)

                response = requests.get(
                    os.path.join(domain, 'catalog/{0}'.format(tag.slug))
                )
                self.assertEqual(response.status_code, 200)

            elif tag.kind in ['3', '9', 'd']:
                response = requests.get(
                    os.path.join(domain, 'filter/{0}'.format(tag.uid))
                )

                self.assertEqual(response.status_code, 200)

            response = requests.get(
                os.path.join(domain, 'label/{0}/{1}'.format(tag.kind, tag.slug))
            )
            self.assertEqual(response.status_code, 200)

    def test_category_j(self):
        for kind in post_cfg.keys():
            response = requests.get(
                os.path.join(domain, 'category_j/{0}/list'.format(kind))
            )

            self.assertEqual(response.status_code, 200)

    def test_classify(self):
        response = requests.get(os.path.join(domain, 'classify/list'))
        self.assertEqual(response.status_code, 200)
