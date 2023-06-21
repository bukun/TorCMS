# -*- coding:utf-8 -*-
from torcms.core import tools
from torcms.model.post_model import MPost
from torcms.model.reply2user_model import MReply2User
from torcms.model.reply_model import MReply
from torcms.model.replyid_model import MReplyid
from torcms.model.user_model import MUser


class TestMReply():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')

        self.uid = tools.get_uuid()
        self.post_id = '1q2w'
        self.username = 'lopk'
        self.user_id = ''
        self.reply_uid = ''
        self.reply_id_uid = ''
        self.add_message()

    def add_message(self, **kwargs):
        post_data = {
            'user_name': self.username,
            'user_pass': kwargs.get('user_pass', 'g131322'),
            'user_email': kwargs.get('user_email', '4256775@kljhqq.com'),
        }

        MUser.create_user(post_data)
        aa = MUser.get_by_name(self.username)
        self.user_id = aa.uid
        p_d = {
            'title': kwargs.get('title', 'iiiii'),
            'cnt_md': kwargs.get('cnt_md', 'grgr'),
            'time_create': kwargs.get('time_create', '1992'),
            'time_update': kwargs.get('time_update', '1996070600'),
            'user_name': kwargs.get('user_name', 'ngng'),
            'view_count': kwargs.get('view_count', 1),
            'logo': kwargs.get('logo', 'prprprprpr'),
            'memo': kwargs.get('memo', ''),
            'order': kwargs.get('order', '1'),
            'keywords': kwargs.get('keywords', ''),
            'extinfo': kwargs.get('extinfo', {}),
            'kind': kwargs.get('kind2', '1'),
            'valid': kwargs.get('valid', 1),

        }

        MPost.add_or_update(self.post_id, p_d)
        post_reply = {
            'post_id': self.post_id,
            'user_name': self.username,
            'user_id': self.user_id,
            'cnt_reply': 'daswrevwefgfgff'
        }
        self.reply_uid = MReply.create_reply(post_reply)
        MReplyid.create_replyid(self.post_id, self.reply_uid)
        aa = MReplyid.get_by_rid(self.post_id)
        for i in aa:
            if i.reply1 == self.reply_uid:
                self.reply_id_uid = i.reply0
        MReply2User.create_reply(self.user_id, self.reply_uid)

    def test_create_reply(self):

        aa = MReply.query_by_post(self.post_id)
        tf = False
        for i in aa:
            if i.uid == self.reply_uid:
                tf = True

        assert tf

    def test_get_by_uid(self):

        aa = MReply.get_by_uid(self.reply_uid)
        assert aa.uid == self.reply_uid
        assert aa.post_id == self.post_id
        assert aa.user_name == self.username

    def test_query_by_post(self):

        aa = MReply.query_by_post(self.post_id)
        tf = False
        for i in aa:
            if i.uid == self.reply_uid:
                tf = True

        assert tf

    def test_get_by_zan(self):
        a = MReply.get_by_zan(self.reply_uid)
        assert a >= 1

    def test_query_all(self):
        aa = MReply.query_all()
        tf = False
        for i in aa:
            if i.uid == self.reply_uid:
                tf = True

        assert tf

    def test_count_of_certain(self):
        a = MReply.count_of_certain()

        assert a >= 1

    def test_total_number(self):
        a = MReply.total_number()

        assert a >= 1

    def test_query_pager(self):

        aa = MReply.query_pager()
        tf = False
        for i in aa:
            if i.uid == self.reply_uid:
                tf = True

        assert tf

    def test_update_vote(self):

        MReply.update_vote(self.reply_uid, 8)
        aa = MReply.query_all()
        tf = False
        for i in aa:
            if i.uid == self.reply_uid:
                tf = True
                assert i.vote == 8

        assert tf

    def test_modify_by_uid(self):

        aa = MReply.get_by_uid(self.reply_uid)
        assert aa.uid == self.reply_uid
        assert aa.post_id == self.post_id
        assert aa.user_name == self.username
        post_reply = {
            'category': '1234',
            'user_name': 'pink',
            'user_id': '8900',
            'cnt_reply': 'hahah'
        }
        MReply.modify_by_uid(self.reply_uid, post_reply)
        aa = MReply.get_by_uid(self.reply_uid)
        assert aa.user_name == 'pink'
        assert aa.category == '1234'
        assert aa.user_id == '8900'

    def test_delete_by_uid(self):

        aa = MReply.query_all()
        tf = False
        for i in aa:
            if i.uid == self.reply_uid:
                tf = True
        assert tf
        MReply.delete_by_uid(self.reply_uid)
        aa = MReply.get_by_uid(self.reply_uid)
        assert aa == None

    def teardown_method(self):
        print("function teardown")
        MUser.delete_by_user_name(self.username)
        MPost.delete(self.post_id)
        MReply2User.delete(self.reply_uid)
        MReply.delete_by_uid(self.reply_uid)
