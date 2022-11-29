# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.entity_model import MEntity


class TestMEntity():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = tools.get_uu4d()
        self.path = 'path'

    def test_create_entity(self):
        uid = self.uid
        post_data = {
            'path': self.path,

        }

        MEntity.create_entity(uid, post_data['path'])
        assert True
        self.tearDown()

    def test_create_entity_2(self):
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
        self.tearDown()

    def test_get_by_uid(self):
        MEntity.get_by_uid(self.uid)
        assert True

    def test_query_all(self):
        MEntity.query_all()
        assert True

    def test_get_by_kind(self):
        MEntity.get_by_kind('2')
        assert True

    def test_get_all_pager(self):
        MEntity.get_all_pager()
        assert True

    def test_get_id_by_impath(self):
        MEntity.get_id_by_impath(self.path)
        assert True

    def test_total_number(self):
        MEntity.total_number()
        assert True

    def test_delete(self):
        MEntity.delete(self.uid)
        assert True

    def test_delete_by_path(self):
        MEntity.delete_by_path(self.path)
        assert True

    def tearDown(self):
        print("function teardown")
        tt = MEntity.get_id_by_impath(self.path)
        if tt:
            MEntity.delete(tt.uid)
