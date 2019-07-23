# -*- coding:utf-8 -*-
from torcms.model.usage_model import MUsage
from torcms.core import tools


class TestMUsage():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')

        self.postid = '12345'
        self.userid = tools.get_uuid()
        self.uid = tools.get_uuid()

    def test_query_by_post(self):
        MUsage.query_by_post(self.postid)
        assert True

    def test_get_all(self):
        MUsage.get_all()
        assert True

    def test_query_random(self):
        MUsage.query_random()
        assert True

    def test_query_recent(self):
        MUsage.query_recent(self.userid, '1')
        assert True

    def test_query_recent_by_cat(self):
        MUsage.query_recent_by_cat(self.userid, '0100', 8)
        assert True

    def test_query_most(self):
        MUsage.query_most(self.userid, '0100', 8)
        assert True

    def test_query_by_signature(self):
        MUsage.query_by_signature(self.userid, self.postid)
        assert True

    def test_count_increate(self):
        MUsage.count_increate(self.uid, '0100', 8)
        assert True

    def test_add_or_update(self):
        MUsage.add_or_update(self.userid, self.postid, '1')
        assert True

    def test_update_field(self):
        MUsage.update_field(self.uid, self.postid)
        assert True
