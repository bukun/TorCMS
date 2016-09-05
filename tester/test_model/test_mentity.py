# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.picture_model import MEntity
import tornado.escape


class TestEntity():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uu = MEntity()
        self.uid = tools.get_uu4d()
        self.imgpath = 'imgpath'

    def test_insert(self):
        uid = self.uid
        post_data = {
            'imgpath': self.imgpath,

        }

        self.uu.insert_data(uid, post_data['imgpath'])
        assert True

    def test_insert_2(self):
        '''Wiki insert: Test invalid title'''
        post_data = {
            'imgpath': '',
        }
        uu = self.uu.get_id_by_impath(post_data['imgpath'])
        assert uu == False

        post_data = {
            'imgpath': self.imgpath,
        }
        uu = self.uu.get_id_by_impath(post_data['imgpath'])
        assert uu == False

    def test_upate(self):
        assert True

    def tearDown(self):
        print("function teardown")
        tt = self.uu.get_id_by_impath(self.imgpath)
        self.uu.delete(tt)
