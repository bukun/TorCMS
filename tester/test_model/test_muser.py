# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.user_model import MUser
import tornado.escape
import time


class TestMUser():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uu = MUser()
        self.username = 'namea'
        self.uid=''

    def test_create_user(self):
        post_data = {
            'user_name': self.username,
            'user_pass': 'g131322',
            'user_email': 'name@kljhqq.com',
        }

        tt = self.uu.create_user(post_data)

        assert tt['success'] == True
        self.tearDown()

    def add_mess(self ,**kwargs):
        name=kwargs.get('user_name',self.username)
        post_data = {
            'user_name': name,
            'user_pass': kwargs.get('user_pass','g131322'),
            'user_email': kwargs.get('user_email','name@kljhqq.com'),
        }

        self.uu.create_user(post_data)
        aa=self.uu.get_by_name(name)
        self.uid=aa.uid

    def test_create_user2(self):
        post_data = {
            'user_name': '',
            'user_pass': 'g131322',
            'user_email': 'name@qkjhlq.com',
        }

        tt = self.uu.create_user(post_data)
        assert tt['success'] == False

        post_data = {
            'user_name': '天',
            'user_pass': 'g131322',
            'user_email': 'name@qhjq.com',
        }

        tt = self.uu.create_user(post_data)
        assert tt['success'] == False

        post_data = {
            'user_name': '/sdfadf',
            'user_pass': 'g131322',
            'user_email': 'name@qjhgq.com',
        }

        tt = self.uu.create_user(post_data)
        assert tt['success'] == False
        self.tearDown()

    def test_update_info(self):
        post_data = {
            'user_email': 'ssadfs@163.com'
        }
        self.add_mess()
        user_info = self.uu.get_by_name(self.username)
        tt = self.uu.update_info(user_info.uid, post_data['user_email'])
        assert tt['success'] == True
        self.tearDown()

    def test_update_pass(self):
        self.add_mess()
        post_data = {
            'user_pass': 'sdfsdfsdf'
        }
        self.uu.update_pass(self.uid,  post_data['user_pass'])
        tt =self.uu.get_by_uid(self.uid)
        assert tt.user_pass==tools.md5(post_data['user_pass'])
        self.tearDown()

    def test_update_role(self):
        post_data = {
            'role': '1111'
        }
        tt = self.uu.update_role(self.username, post_data['role'])
        assert tt == True
        self.tearDown()

    # def test_total_number(self):
    #     self.uu.total_number()
    #
    #
    # def test_query_pager_by_slug(self):
    #     self.uu.query_pager_by_slug()
    #
    # def test_count_of_certain(self):
    #     self.uu.count_of_certain()
    #
    # def test_delete(self):
    #     self.uu.delete()
    #
    # def test_delete_by_user_name(self):
    #     self.uu.delete_by_user_name()
    #
    # def test_get_by_keyword(self):
    #     self.uu.get_by_keyword()
    #
    # def test_update_time_login(self):
    #     self.uu.update_time_login()
    #
    # def test_update_time_reset_passwd(self):
    #     self.uu.update_time_reset_passwd()
    #
    # def test_query_nologin(self):
    #     self.uu.query_nologin()
    #
    # def test_check_user_by_email(self):
    #     self.uu.check_user_by_email()
    #
    # def test_check_user_by_name(self):
    #     self.uu.check_user_by_name()
    #
    # def test_check_user(self):
    #     self.uu.check_user()
    #
    # def test_get_by_email(self):
    #     self.uu.get_by_email()

    def test_set_sendemail_time(self):
        self.add_mess()
        bb= self.uu.get_by_uid(self.uid)

        time.sleep(2)
        aa=self.uu.set_sendemail_time(self.uid)
        aa = self.uu.get_by_uid(self.uid)
        assert bb.time_email<=aa.time_email
        self.tearDown()

    def test_get_by_name(self):
        self.add_mess()
        aa=self.uu.get_by_name(self.username)
        assert aa.uid==self.uid
        self.tearDown()

    def test_get_by_uid(self):
        self.add_mess()
        aa=self.uu.get_by_uid(self.uid)
        assert aa.user_name==self.username
        self.tearDown()

    def test_query_all(self):
        aa=self.uu.query_all()
        tf=True
        for i in aa:
            if i.user_name==self.username:
                tf=False
        assert tf
        self.add_mess()
        aa = self.uu.query_all()
        tf = False
        for i in aa:
            if i.user_name == self.username:
                tf = True
        assert tf
        self.tearDown()

    def tearDown(self):
        print("function teardown")
        tt=self.uu.get_by_uid(self.uid)
        if tt:
            self.uu.delete(tt.uid)
        self.uu.delete_by_user_name(self.username)
