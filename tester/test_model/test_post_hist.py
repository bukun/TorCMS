# -*- coding:utf-8 -*-
from torcms.model.post_hist_model import MPostHist
from torcms.core import tools


class TestMPostHist():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = tools.get_uuid()
        self.post_id = '11111'

    def test_create_post_history(self):
        assert True

    def test_get_by_uid(self):
        MPostHist.get_by_uid(self.uid)
        assert True

    def test_update_cnt(self):
        post_data = {
            'user_name': 'giser',
            'cnt_md': 'gisersdfsdfsdf'
        }
        MPostHist.update_cnt(self.uid, post_data)
        assert True

    def test_query_by_postid(self):
        MPostHist.query_by_postid(self.post_id)
        assert True

    def test_get_last(self):
        MPostHist.get_last(self.post_id)
        assert True

    def tearDown(self):
        print("function teardown")
        tt = MPostHist.get_by_uid(self.uid)
        if tt:
            MPostHist.delete(self.uid)
