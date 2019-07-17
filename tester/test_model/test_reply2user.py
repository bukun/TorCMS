# -*- coding:utf-8 -*-
from torcms.model.reply2user_model import MReply2User


class TestMReply2User():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')

        self.app_f = '12345'
        self.app_t = '65412'

    def test_add_relation(self):
        MReply2User.add_relation(self.app_f, self.app_t)
        assert True