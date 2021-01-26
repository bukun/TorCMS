# -*- coding:utf-8 -*-

from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabReplyid
from torcms.model.replyid_model import MReplyid


class TestMReplyid():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = ''
        self.reply0 = 'notok'
        self.reply1 = 'nothapppy'

    def add_message(self, **kwargs):
        MReplyid.create_replyid(self.reply0, self.reply1)
        aa = MReplyid.get_by_rid(self.reply0)
        for i in aa:
            if i.reply1 == self.reply1:
                self.uid = i.uid
                return i

    def test_get_by_uid(self):
        aa = self.add_message()
        b = MReplyid.get_by_uid(aa.uid)
        assert b.reply0 == self.reply0
        assert b.reply1 == self.reply1
        self.tearDown()

    def test_create_replyid(self):
        aa = self.add_message()
        assert aa.reply1 == self.reply1
        self.tearDown()

    def test_get_by_rid(self):
        self.add_message()
        aa = MReplyid.get_by_rid(self.reply0)
        for i in aa:
            if i.reply1 == self.reply1:
                assert i.uid == self.uid
        self.tearDown()

    def tearDown(self):
        print("function teardown")
        MHelper.delete(TabReplyid, self.uid)
        self.uid = ''
