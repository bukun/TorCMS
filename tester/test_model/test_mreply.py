# -*- coding:utf-8 -*-

import tornado.escape
import tornado.web

from torcms.core import tools
from torcms.model.post_model import MPost
from torcms.model.reply2user_model import MReply2User
from torcms.model.reply_model import MReply
from torcms.model.user_model import MUser


class TestMReply():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.post = MPost()
        self.user = MUser()
        self.reply = MReply()
        self.r2u = MReply2User()

        self.post_title = 'fwwgccc'
        self.username = 'adminsadfl'
        self.user_uid = ''
        self.reply_uid = ''
        self.post_uid = '998h'
        self.password = 'g131322'

        self.add_post()
        self.add_user()
        self.add_reply()

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

    def add_post(self, **kwargs):
        p_d = {
            'title': kwargs.get('title', self.post_title),
            'cnt_md': kwargs.get('cnt_md', 'grgr'),
            'time_create': kwargs.get('time_create', '1992'),
            'time_update': kwargs.get('time_update', '1996070600'),
            'user_name': self.username,
            'view_count': kwargs.get('view_count', 1),
            'logo': kwargs.get('logo', 'prprprprpr'),
            'memo': kwargs.get('memo', ''),
            'order': kwargs.get('order', '1'),
            'keywords': kwargs.get('keywords', 'sd,as'),
            'extinfo': kwargs.get('extinfo', {}),
            'kind': kwargs.get('kind', '1'),
            'valid': kwargs.get('valid', 1),

        }

        MPost.add_or_update(self.post_uid, p_d)

    def test_insert_post(self):
        # raw_count = self.post.get_counts()

        tt = self.post.get_by_uid(self.post_uid)
        assert tt.title == self.post_title

    def test_insert_user(self):

        tt = self.user.get_by_uid(self.user_uid)
        assert tt.user_name == self.username

    def add_reply(self, **kwargs):
        p_d = {
            'post_id': self.post_uid,
            'user_name': self.username,
            'user_id': self.user_uid,
            'category': '0',
            'cnt_reply': kwargs.get('cnt_reply', 'f4klkj进口国海关好姐姐4'),
        }
        uid = self.reply.create_reply(p_d)
        self.reply_uid = uid
        self.r2u.create_reply(self.user_uid, uid)

    def test_insert_reply(self):

        aa = self.reply.get_by_uid(self.reply_uid)
        assert aa.user_name == self.username
        assert aa.post_id == self.post_uid
        assert aa.user_id == self.user_uid

    def test_update_vote(self):

        before = self.reply.get_by_uid(self.reply_uid)
        self.reply.update_vote(self.reply_uid, 10)
        after = self.reply.get_by_uid(self.reply_uid)
        assert after.vote == 10
        assert before.vote < after.vote

    def test_delete_by_uid(self):

        yesrep = self.reply.get_by_uid(self.reply_uid)
        assert yesrep.post_id == self.post_uid
        aa = self.reply.delete_by_uid(self.reply_uid)
        assert aa
        nosrep = self.reply.get_by_uid(self.reply_uid)
        assert nosrep == None

    def test_modify_by_uid(self):

        p_d = {
            'user_name': self.username,
            'user_id': self.user_uid,
            'category': '1',
            'cnt_reply': '一二三四',
        }
        aa = self.reply.modify_by_uid(self.reply_uid, p_d)
        assert aa == self.reply_uid
        tt = self.reply.get_by_uid(self.reply_uid)
        assert tt.category == p_d['category']
        assert tt.cnt_md == p_d['cnt_reply']

    def test_query_pager(self):

        aa = self.reply.total_number()
        a = int(aa / 10)
        tf = False
        for i in range(a + 3):

            list = self.reply.query_pager(current_page_num=i)
            for x in list:
                if x.uid == self.reply_uid:
                    tf = True
                    break

        assert tf

    def test_total_number(self):
        aa = self.reply.total_number()

        assert aa >= 1

    def test_count_of_certain(self):
        aa = self.reply.count_of_certain()

        assert aa >= 1

    def test_query_all(self):

        bb = self.reply.query_all()
        tf = False
        for i in bb:
            if i.uid == self.reply_uid:
                tf = True
                assert i.post_id == self.post_uid
                break
        assert tf

    def test_get_by_zan(self):

        aa = self.reply.get_by_zan(self.reply_uid)
        assert aa >= 1

    def test_query_by_post(self):

        aa = self.reply.query_by_post(self.post_uid)
        tf = False
        for i in aa:
            if i.uid == self.reply_uid:
                tf = True
                break
        assert tf

    def test_get_by_uid(self):

        aa = self.reply.get_by_uid(self.reply_uid)
        assert aa.user_id == self.user_uid

    def teardown_method(self):
        print("function teardown")
        tt = self.post.get_by_uid(self.post_uid)
        if tt:
            self.post.delete(tt.uid)
        self.user.delete_by_user_name(self.username)
        tt = self.user.get_by_uid(self.user_uid)
        if tt:
            self.user.delete(tt.uid)
        tt = self.reply.get_by_uid(self.reply_uid)
        if tt:
            self.reply.delete_by_uid(tt.uid)
        self.r2u.delete(self.reply_uid)
