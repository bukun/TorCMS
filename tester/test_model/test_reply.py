# -*- coding:utf-8 -*-
from torcms.model.reply_model import MReply
from torcms.core import tools


class TestMReply():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')

        self.uid = tools.get_uuid()

    def test_create_reply(self):
        post_data = {
            'post_id': '11111',
            'user_name': 'giser',
            'user_id': 'ddadsaweadqw',
            'cnt_reply': 'gisersdasdasdasdzxcsdwdqgiser',
        }
        MReply.create_reply(post_data)
        assert True

    def test_get_by_uid(self):
        MReply.get_by_uid(self.uid)
        assert True

    def test_query_by_post(self):
        MReply.query_by_post(self.uid)
        assert True

    def test_get_by_zan(self):
        MReply.get_by_zan(self.uid)
        assert True

    def test_query_all(self):
        MReply.query_all()
        assert True

    def test_count_of_certain(self):
        MReply.count_of_certain()
        assert True

    def test_total_number(self):
        MReply.total_number()
        assert True

    def test_query_pager(self):
        MReply.query_pager()
        assert True

    def test_update_vote(self):
        MReply.update_vote(self.uid, 8)
        assert True

    def test_delete(self):
        MReply.delete(self.uid)
        assert True
