# -*- coding:utf-8 -*-
from torcms.model.collect_model import MCollect
from torcms.core import tools


class TestMCollect():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = tools.get_uu4d()

    def test_query_recent(self):
        user_id = '11111'
        MCollect.query_recent(user_id)
        assert True
    