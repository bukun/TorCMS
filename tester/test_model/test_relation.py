# -*- coding:utf-8 -*-
from torcms.model.relation_model import MRelation


class TestMRelation():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')

        self.app_f = '12345'
        self.app_t = '65412'

    def test_add_relation(self):
        MRelation.add_relation(self.app_f, self.app_t)
        assert True

    def test_update_relation(self):
        MRelation.update_relation(self.app_f, self.app_t)
        assert True

    def test_get_app_relations(self):
        MRelation.get_app_relations(self.app_f)
        assert True

    def test_delete(self):
        MRelation.delete(self.app_f)
        assert True
