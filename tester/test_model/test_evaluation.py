# -*- coding:utf-8 -*-
from torcms.model.evaluation_model import MEvaluation


class TestMEvaluation():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.user_id = '11111'
        self.app_id = 'a1234'

    def test_app_evaluation_count(self):
        MEvaluation.app_evaluation_count(self.app_id)
        assert True

    def test_get_by_signature(self):
        MEvaluation.get_by_signature(self.user_id, self.app_id)
        assert True

    def test_add_or_update(self):
        value = 1
        MEvaluation.add_or_update(self.user_id, self.app_id, value)
        assert True
