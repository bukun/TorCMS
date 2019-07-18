# -*- coding:utf-8 -*-
from torcms.model.reply2user_model import MReply2User


class TestMReply2User():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')

        self.user_id = '12345'
        self.reply_id = '65412'

    def test_create_reply(self):
        MReply2User.create_reply(self.user_id, self.reply_id)
        assert True

    def test_get_voter_count(self):
        MReply2User.get_voter_count(self.reply_id)
        assert True

    def tearDown(self):
        print("function teardown")

        MReply2User.delete(self.reply_id)
