# -*- coding:utf-8 -*-
from torcms.model.collect_model import MCollect



class TestMCollect():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.user_id = '11111'

    def test_query_recent(self):
        user_id = self.user_id
        MCollect.query_recent(user_id)
        assert True

    def test_get_by_signature(self):
        user_id = self.user_id
        app_id = '11111'
        MCollect.get_by_signature(user_id, app_id)
        assert True

    def test_count_of_user(self):
        user_id = self.user_id
        MCollect.count_of_user(user_id)
        assert True

    def test_query_pager_by_all(self):
        user_id = self.user_id
        MCollect.query_pager_by_all(user_id)
        assert True

    def test_add_or_update(self):
        user_id = self.user_id
        app_id = '11111'
        MCollect.add_or_update(user_id, app_id)
        assert True

    def test_query_pager_by_userid(self):
        user_id = self.user_id
        kind = '1'
        MCollect.query_pager_by_userid(user_id, kind)
        assert True
