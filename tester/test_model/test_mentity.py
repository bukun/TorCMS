# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.entity_model import MEntity


class TestEntity():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = tools.get_uu4d()
        self.path = 'path'

    def test_insert(self):
        uid = self.uid
        post_data = {
            'path': self.path,

        }

        MEntity.create_entity(uid, post_data['path'])
        assert True

    def test_insert_2(self):
        '''Wiki insert: Test invalid title'''
        post_data = {
            'path': '',
        }
        uu = MEntity.get_id_by_impath(post_data['path'])
        assert uu is None

        post_data = {
            'path': self.path,
        }
        uu = MEntity.get_id_by_impath(post_data['path'])
        assert uu is None

    def test_upate(self):
        assert True

    def tearDown(self):
        print("function teardown")
        tt = MEntity.get_id_by_impath(self.path)
        if tt:
            print('x' * 20)
            print(tt)
            MEntity.delete(tt)
