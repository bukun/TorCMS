# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.post_model import MPost
from torcms.model.reply_model import MReply
from torcms.model.user_model import MUser
import tornado.escape


class TestPost():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.post = MPost()
        self.user = MUser()
        self.reply = MReply()

        self.post_title = 'ccc'
        self.username = 'adminsadfl'
        self.uid = tools.get_uu4d()



    # def test_insert_post(self):
    #     # raw_count = self.post.get_counts()
    #
    #     post_data = {
    #         'title': self.post_title,
    #         'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
    #         'user_name': 'Tome',
    #         'view_count': 1,
    #         'logo': '/static/',
    #         'keywords': 'sdf',
    #
    #     }
    #     self.post.insert_data(self.uid, post_data)
    #
    #
    #     tt = self.post.get_by_uid(self.uid)

    def test_insert_user(self):

        post_data = {
            'user_name':self.username,
            'user_pass':'g131322',
            'user_email':'nahme@qkhlkq.com',
        }


        tt=self.user.create_user(post_data)


        print('=' * 20)
        print(tt)
        assert tt['success'] == True


    def test_insert_reply(self):

        post_data = {
            'user_name':self.username,
            'user_pass':'g131322',
            'user_email':'name@qlkjq.com',
        }


        tt=self.user.create_user(post_data)


        # u_id = self.user.get_by_name(self.username)
        #
        #
        # self.userid = u_id.uid
        #
        # print("*" * 50)
        # print(self.userid)
        # print("*" * 50)
        # post_data = {
        #     'user_name':[self.username],
        #     'create_user_id':[self.userid],
        #     'timestamp':['2'],
        #     'date':['1'],
        #     'cnt_md':['###adfafasf/sdf'],
        #     'cnt_html':['###adfafasf/sdf'],
        #     'vote':0,
        # }





    def test_upate(self):
        assert True

    def tearDown(self):
        print("function teardown")
        tt = self.post.get_by_uid(self.uid)
        if tt:
            self.post.delete(tt.uid)
        self.user.delete_by_user_name(self.username)
