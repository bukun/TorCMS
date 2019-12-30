# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.post_model import MPost
from torcms.model.reply_model import MReply
from torcms.model.user_model import MUser
import tornado.escape


class TestMReply():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.post = MPost()
        self.user = MUser()
        self.reply = MReply()

        self.post_title = 'fwwgccc'
        self.username = 'adminsadfl'
        self.user_uid=''
        self.reply_uid = ''
        self.post_uid='35j9'

    def add_user(self ,**kwargs):
        name=kwargs.get('user_name',self.username)
        post_data = {
            'user_name': name,
            'user_pass': kwargs.get('user_pass','g131322'),
            'user_email': kwargs.get('user_email','name@kljhqq.com'),
        }

        self.user.create_user(post_data)
        aa=self.user.get_by_name(name)
        self.user_uid=aa.uid


    def add_post(self,**kwargs):
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

        MPost.create_post(self.post_uid, p_d)

    def test_insert_post(self):
        # raw_count = self.post.get_counts()

        self.add_post()
        tt = self.post.get_by_uid(self.post_uid)
        assert tt.title==self.post_title
        self.tearDown()

    def test_insert_user(self):

        self.add_user()
        tt=self.user.get_by_uid(self.user_uid)
        assert tt.user_name==self.username
        self.tearDown()

    def add_reply(self,**kwargs):
        p_d = {
            'post_id': self.post_uid,
            'user_name':self.username,
            'user_id': self.user_uid,
            'category': kwargs.get('category', '0'),

            'cnt_reply': kwargs.get('cnt_reply', 'nininininin'),


        }
        uid=self.reply.create_reply(p_d)
        self.reply_uid=uid
    #
    # def test_insert_reply(self):
    #
    #     self.tearDown()
    #     self.add_user()
    #     self.add_post()
    #     self.add_reply()
    #     aa=self.reply.get_by_uid(self.reply_uid)
    #     assert aa.user_name==self.username
    #     assert aa.post_id==self.post_uid
    #     assert aa.user_id==self.user_uid
    #     self.tearDown()


    #
    # def test_update_vote(self):
    #     self.reply.update_vote()
    #     assert True
    #
    #
    # def test_delete_by_uid(self):
    #     self.reply.delete_by_uid()
    #     assert True
    #
    #
    # def test_modify_by_uid(self):
    #     self.reply.modify_by_uid()
    #     assert True
    #

    def test_query_pager(self):
        self.reply.query_pager()
        assert True


    def test_total_number(self):
        self.reply.total_number()
        assert True


    def test_count_of_certain(self):
        self.reply.count_of_certain()
        assert True
    #
    # def test_delete(self):
    #     self.reply.delete()
    #     assert True
    #
    # def test_query_all(self):
    #     self.reply.query_all()
    #     assert True
    #
    # def test_get_by_zan(self):
    #     self.reply.get_by_zan()
    #     assert True
    #
    # def test_query_by_post(self):
    #     self.reply.query_by_post()
    #     assert True
    #

    #
    # def test_get_by_uid(self):
    #     self.reply.get_by_uid()
    #     assert True

    def tearDown(self):
        print("function teardown")
        tt = self.post.get_by_uid(self.post_uid)
        if tt:
            self.post.delete(tt.uid)
        self.user.delete_by_user_name(self.username)
        tt = self.user.get_by_uid(self.user_uid)
        if tt:
            self.user.delete(tt.uid)
        tt=self.reply.get_by_uid(self.reply_uid)
        if tt:
            self.reply.delete(tt.uid)
