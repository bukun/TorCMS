# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.post_model import MPost
from torcms.model.reply_model import MReply
from torcms.model.user_model import MUser
from torcms.model.reply2user_model import MReply2User
import tornado.web
import tornado.escape


class TestMReply():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.post = MPost()
        self.user = MUser()
        self.reply = MReply()
        self.r2u=MReply2User()

        self.post_title = 'fwwgccc'
        self.username = 'adminsadfl'
        self.user_uid=''
        self.reply_uid = ''
        self.post_uid='998h'
        self.password='g131322'

    def add_user(self ,**kwargs):
        name=kwargs.get('user_name',self.username)
        post_data = {
            'user_name': name,
            'user_pass': kwargs.get('user_pass',self.password),
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
            'category':'0',
            'cnt_reply': kwargs.get('cnt_reply', 'f4klkj进口国海关好姐姐4'),
         }
        uid=self.reply.create_reply(p_d)
        self.reply_uid=uid
        self.r2u.create_reply(self.user_uid,uid)


    def test_insert_reply(self):

        self.add_user()
        self.add_post()
        self.add_reply()
        aa=self.reply.get_by_uid(self.reply_uid)
        assert aa.user_name==self.username
        assert aa.post_id==self.post_uid
        assert aa.user_id==self.user_uid
        self.tearDown()



    def test_update_vote(self):
        self.add_user()
        self.add_post()
        self.add_reply()
        before=self.reply.get_by_uid(self.reply_uid)
        self.reply.update_vote(self.reply_uid,10)
        after=self.reply.get_by_uid(self.reply_uid)
        assert after.vote==10
        assert before.vote<after.vote
        self.tearDown()


    def test_delete_by_uid(self):
        self.add_user()
        self.add_post()
        self.add_reply()
        yesrep=self.reply.get_by_uid(self.reply_uid)
        assert yesrep.post_id==self.post_uid
        aa=self.reply.delete_by_uid(self.reply_uid)
        assert aa
        nosrep = self.reply.get_by_uid(self.reply_uid)
        assert nosrep == None
        self.tearDown()


    def test_modify_by_uid(self):
        self.add_user()
        self.add_post()
        self.add_reply()
        p_d = {
            'user_name': self.username,
            'user_id': self.user_uid,
            'category': '1',
            'cnt_reply': '一二三四',
        }
        aa=self.reply.modify_by_uid(self.reply_uid,p_d)
        assert aa==self.reply_uid
        tt=self.reply.get_by_uid(self.reply_uid)
        assert tt.category==p_d['category']
        assert tt.cnt_md==p_d['cnt_reply']
        self.tearDown()


    def test_query_pager(self):
        self.add_user()
        self.add_post()
        self.add_reply()
        aa = self.reply.total_number()
        a=int(aa/10)
        tf=False
        for i in range(a+3):

            list=self.reply.query_pager(current_page_num=i)
            for x in list:
                if x.uid==self.reply_uid:
                    tf=True
                    break
        self.tearDown()
        assert tf


    def test_total_number(self):
        aa=self.reply.total_number()
        self.add_user()
        self.add_post()
        self.add_reply()
        bb=self.reply.total_number()
        assert aa+1<=bb
        self.tearDown()


    def test_count_of_certain(self):
        aa = self.reply.count_of_certain()
        self.add_user()
        self.add_post()
        self.add_reply()
        bb =self.reply.count_of_certain()
        assert aa + 1 <= bb
        self.tearDown()

    # def test_delete(self):
    #     self.tearDown()
    #     bb = self.reply.count_of_certain()
    #     print(bb)
    #     self.add_user()
    #     self.add_post()
    #     self.add_reply()
    #     bb = self.reply.count_of_certain()
    #     print(bb)
    #     aa=self.reply.get_by_uid(self.reply_uid)
    #     assert aa.post_id==self.post_uid
    #     aa = self.reply.query_by_post(self.post_uid)
    #     tf = False
    #     for i in aa:
    #         if i.uid == self.reply_uid:
    #             tf = True
    #             break
    #     assert tf
    #     vv=self.reply.delete(self.post_uid)
    #     print('LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLl')
    #     print(vv)
    #     s = self.reply.count_of_certain()
    #     print(s)
    #     # assert vv
    #     aa = self.reply.get_by_uid(self.reply_uid)
    #     self.tearDown()
    #     assert aa==None


    def test_query_all(self):
        self.tearDown()

        aa=self.reply.query_all()
        tf = True
        for i in aa:
            if i.uid == self.reply_uid:
                tf = False
                break
        assert tf
        self.add_user()
        self.add_post()
        self.add_reply()
        bb = self.reply.query_all()
        tf=False
        for i in bb:
            if i.uid==self.reply_uid:
                tf=True
                assert i.post_id==self.post_uid
                break
        assert tf
        self.tearDown()

    def test_get_by_zan(self):

        self.add_user()
        self.add_post()
        self.add_reply()
        aa = self.reply.get_by_zan(self.reply_uid)
        assert aa>=1
        self.tearDown()

    def test_query_by_post(self):
        self.add_user()
        self.add_post()
        self.add_reply()
        aa=self.reply.query_by_post(self.post_uid)
        tf=False
        for i in aa:
            if i.uid==self.reply_uid:
                tf=True
                break
        assert tf
        self.tearDown()



    def test_get_by_uid(self):
        self.add_user()
        self.add_post()
        self.add_reply()
        aa=self.reply.get_by_uid(self.reply_uid)
        assert aa.user_id==self.user_uid
        self.tearDown()

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
            self.reply.delete_by_uid(tt.uid)
        self.r2u.delete(self.reply_uid)
