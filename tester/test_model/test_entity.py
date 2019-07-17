# -*- coding:utf-8 -*-
from torcms.core import tools
from torcms.model.entity_model import MEntity


class TestMEntity():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = tools.get_uuid()
        self.path = '/static/'

    def test_create_entity(self):
        uid = self.uid
        path = self.path
        desc = 'create entity'
        kind = '1'
        tt = MEntity.create_entity(uid, path, desc, kind)
        assert tt == True

    def test_query_recent(self):
        MEntity.get_by_uid(self.uid)
        assert True

    def test_query_all(self):
        MEntity.query_all()
        assert True

    def test_get_by_kind(self):
        MEntity.get_by_kind()
        assert True

    def test_get_all_pager(self):
        MEntity.get_all_pager()
        assert True

    def test_get_id_by_impath(self):
        path = self.path
        MEntity.get_id_by_impath(path)
        assert True

    def test_total_number(self):
        MEntity.total_number()
        assert True

    def test_delete_by_path(self):
        MEntity.delete_by_path(self.path)
        assert True

    def tearDown(self):
        print("function teardown")
        tt = MEntity.get_by_uid(self.uid)
        if tt:
            MEntity.delete(tt.uid)
