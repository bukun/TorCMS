# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.app_model import MApp
import tornado.escape


class TestApp():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uu = MApp()

        self.title = '哈哈sdfsdf'
        self.uid = tools.get_uu4d()

    def test_insert(self):
        uid = self.uid
        post_data = {

            'title': self.title,
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'extinfo': ''
        }
        extinfo = {

        }

        self.uu.add_meta(uid, post_data, extinfo)
        tt = self.uu.get_by_uid(uid)
        assert tt == False

    def test_insert2(self):
        uid = self.uid
        post_data = {

            'title': [''],
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'extinfo': ''
        }
        extinfo = {

        }

        self.uu.add_meta(uid, post_data, extinfo)
        tt = self.uu.get_by_uid(uid)
        assert tt == False

        post_data = {
            'title': ['1'],
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'extinfo': ''
        }
        uu = self.uu.add_meta(self.uid, post_data)
        assert uu == False

        post_data = {
            'title': ['天'],
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'extinfo': ''
        }
        uu = self.uu.add_meta(self.uid, post_data)
        assert uu == False

    def test_upate(self):
        assert True

    def tearDown(self):
        print("function teardown")
        tt = self.uu.get_by_uid(self.uid)
        if tt:
            self.uu.delete(tt.uid)
