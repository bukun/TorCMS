import os
from datetime import datetime

import requests
from faker import Faker
from tornado.testing import AsyncHTTPSTestCase

from cfg import SITE_CFG
from config import post_cfg
from server import APP
from torcms.core.tools import get_uu4d, get_uuid
from torcms.model.category_model import MCategory
from torcms.model.post_model import MPost

fak = Faker('zh_CN')

domain = SITE_CFG['site_url']


class TestPostHandler(AsyncHTTPSTestCase):
    def get_app(self):
        return APP

    def test_posthandler_view_edit_delete(self):
        for key in post_cfg:
            if key not in ['2', 's']:
                print(key)
                postinfos = MPost.query_all(kind=key)
                for post in postinfos:
                    the_url = os.path.join(
                        domain, '{0}/{1}'.format(post_cfg[key]['router'], post.uid)
                    )
                    print('=' * 80)
                    print(the_url)
                    print('=' * 80)
                    response = requests.get(the_url)
                    self.assertEqual(response.status_code, 200)

    def test_posthandler_add(self):
        for k in post_cfg:
            for ii in range(3):
                postuid = f'{k}{get_uu4d()}'
                while MPost.get_by_uid(postuid):
                    postuid = f'{k}{get_uu4d()}'

                response = requests.get(
                    os.path.join(
                        domain, '{0}/_add/{1}'.format(post_cfg[k]['router'], postuid)
                    )
                )
                self.assertEqual(response.status_code, 200)
