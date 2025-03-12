import json
import unittest

from tornado.testing import AsyncHTTPTestCase
from torcms.model.category_model import MCategory
from server import APP
from config import post_cfg

tags = MCategory.query_all()


class TestTornado(AsyncHTTPTestCase):
    '''
    标签的访问方式都是以 label/ 开头
    分类的访问方式数据以 filter/开头，文档以 list/开头
    目前只能根据固定kind值区分是数据还是分类。
    '''

    def get_app(self):
        return APP

    def test_category_label(self):

        for tag in tags:

            if tag.kind == '1' or tag.kind == 'm':
                response = self.fetch('/list/{0}'.format(tag.slug))
                self.assertEqual(response.code, 200)

                response = self.fetch('/catalog/{0}'.format(tag.slug))
                self.assertEqual(response.code, 200)

                response = self.fetch('/label/{0}/{1}'.format(tag.kind, tag.slug))
                self.assertEqual(response.code, 200)



            elif tag.kind == '3' or tag.kind == '9':
                response = self.fetch('/filter/{0}'.format(tag.uid))
                self.assertEqual(response.code, 200)

                response = self.fetch('/label/{0}/{1}'.format(tag.kind, tag.slug))
                self.assertEqual(response.code, 200)

    def test_category_j(self):
        for kind in post_cfg.keys():
            response = self.fetch('/category_j/{0}/list'.format(kind))
            self.assertEqual(response.code, 200)

    def test_classify(self):
        for kind in post_cfg.keys():
            response = self.fetch('/classify/list'.format(kind))
            self.assertEqual(response.code, 200)
