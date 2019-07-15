# -*- coding:utf-8 -*-

from torcms.model.relation_model import MRelation
from torcms.core import tools


class TestMRelation():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = tools.get_uu4d()

    def test_add_relation(self):
        app_f = '11111'
        app_t = '12345'
        MRelation.add_relation(app_f, app_t)
        assert True

    def test_update_relation(self):
        app_f = '11111'
        app_t = '12345'
        MRelation.update_relation(app_f, app_t)
        assert True

    def test_get_app_relations(self):
        app_id = '11111'

        MRelation.get_app_relations(app_id)
        assert True

    def test_delete(self):
        app_id = '11111'

        MRelation.delete(app_id)
        assert True
