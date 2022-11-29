# -*- coding:utf-8 -*-
from torcms.model.reply2user_model import MReply2User
from torcms.model.reply_model import MReply
from torcms.model.user_model import MUser


class TestMReply2User():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.user = MUser()
        self.reply = MReply()
        self.r2u = MReply2User()
        self.username = 'adminsadfl'
        self.password = 'g131322'

        self.user_uid = '12345'
        self.reply_uid = '65412'

    def add_user(self, **kwargs):
        name = kwargs.get('user_name', self.username)
        post_data = {
            'user_name': name,
            'user_pass': kwargs.get('user_pass', self.password),
            'user_email': kwargs.get('user_email', 'name@kljhqq.com'),
        }

        self.user.create_user(post_data)
        aa = self.user.get_by_name(name)
        self.user_uid = aa.uid

    def add_reply(self, **kwargs):
        p_d = {
            'post_id': 'gtyu',
            'user_name': self.username,
            'user_id': self.user_uid,
            'category': '0',
            'cnt_reply': kwargs.get('cnt_reply', 'kfjd速度很快很低'),
        }
        uid = self.reply.create_reply(p_d)
        self.reply_uid = uid
        self.r2u.create_reply(self.user_uid, uid)

    def test_create_reply(self):
        self.add_user()
        self.add_reply()
        self.r2u.create_reply(self.user_uid, self.reply_uid)
        aa = self.r2u.get_voter_count(self.reply_uid)
        assert aa >= 1
        self.tearDown()

    #
    # def test_update(self):
    #     self.r2u.update()

    def test_delete(self):
        self.add_user()
        self.add_reply()
        self.r2u.create_reply(self.user_uid, self.reply_uid)
        aa = self.r2u.get_voter_count(self.reply_uid)
        assert aa >= 1
        self.r2u.delete(self.reply_uid)
        aa = self.r2u.get_voter_count(self.reply_uid)
        assert aa == 0
        self.tearDown()

    def test_get_voter_count(self):
        self.add_user()
        self.add_reply()
        self.r2u.create_reply(self.user_uid, self.reply_uid)
        aa = self.r2u.get_voter_count(self.reply_uid)
        assert aa >= 1
        self.tearDown()

    def tearDown(self):
        print("function teardown")
        tt = self.user.get_by_uid(self.user_uid)
        if tt:
            self.user.delete(tt.uid)
        tt = self.reply.get_by_uid(self.reply_uid)
        if tt:
            self.reply.delete_by_uid(tt.uid)
        self.r2u.delete(self.reply_uid)
