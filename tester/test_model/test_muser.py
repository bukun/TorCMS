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
        self.add_mess()
        post_data = {
            'role': '1111'
        }
        self.uu.update_role(self.username, post_data['role'])
        tt = self.uu.get_by_uid(self.uid)
        assert tt.role == post_data['role']
        self.tearDown()

    def test_total_number(self):
        a=self.uu.total_number()
        self.add_mess()
        b=self.uu.total_number()
        assert a+1<=b
        self.tearDown()


    def test_query_pager_by_slug(self):
        self.add_mess()
        a = self.uu.total_number()
        x=int(a/10)
        tf=False
        for i in range(x+2):

            aa=self.uu.query_pager_by_slug(current_page_num=i)
            for y in aa:
                if y.uid==self.uid:
                    tf=True
        self.tearDown()
        assert tf


    def test_count_of_certain(self):
        a=self.uu.count_of_certain()
        self.add_mess()
        b=self.uu.count_of_certain()
        assert a+1<=b
        self.tearDown()

    def test_delete(self):
        user_info = self.uu.get_by_name(self.username)
        self.add_mess()
        user_info2 = self.uu.get_by_name(self.username)
        aa=self.uu.delete(self.uid)
        user_info3 = self.uu.get_by_name(self.username)
        assert aa == True
        assert user_info==user_info3
        assert user_info==None
        assert user_info2.uid==self.uid
        self.tearDown()

    def test_delete_by_user_name(self):
        user_info = self.uu.get_by_name(self.username)
        self.add_mess()
        user_info2 = self.uu.get_by_name(self.username)
        aa=self.uu.delete_by_user_name(self.username)
        user_info3 = self.uu.get_by_name(self.username)
        assert aa==True
        assert user_info == user_info3
        assert user_info == None
        assert user_info2.uid == self.uid
        self.tearDown()

    def test_get_by_keyword(self):
        self.add_mess()
        aa=self.uu.get_by_keyword('me')
        tf=False
        for i in aa:
            if i.uid==self.uid:
                tf=True
        self.tearDown()
        assert tf


    def test_update_time_login(self):
        self.add_mess()
        user_info = self.uu.get_by_name(self.username)
        time.sleep(2)
        self.uu.update_time_login(self.username)
        aa = self.uu.get_by_name(self.username)
        assert user_info.time_login!=aa.time_login
        self.tearDown()

    def test_update_time_reset_passwd(self):
        self.add_mess()
        time_r=11111111
        aa=self.uu.update_time_reset_passwd(self.username,time_r)
        assert aa==True
        aa = self.uu.get_by_name(self.username)
        assert aa.time_reset_passwd==time_r
        self.tearDown()

    def test_query_nologin(self):
        aa=self.uu.query_nologin()
        self.add_mess()
        bb=self.uu.query_nologin()
        assert aa.count()==bb.count()
        self.tearDown()

    def test_check_user_by_email(self):
        post_data = {
            'user_email': 'ssadfs@163.com',
            'user_pass':'ffffff'
        }
        self.add_mess(**post_data)
        aa=self.uu.check_user_by_email(post_data['user_email'],post_data['user_pass'])
        assert aa==1
        self.tearDown()

    def test_check_user_by_name(self):
        post_data = {
            'user_pass': 'ffffff'
        }
        self.add_mess(**post_data)
        aa=self.uu.check_user_by_name(self.username,post_data['user_pass'])
        assert aa == 1
        self.tearDown()

    def test_check_user(self):
        post_data = {
            'user_pass': 'ffffff'
        }
        self.add_mess(**post_data)
        aa=self.uu.check_user(self.uid,post_data['user_pass'])
        assert aa == 1
        self.tearDown()

    def test_get_by_email(self):
        post_data = {
            'user_email': 'ssadfs@163.com'
        }
        self.add_mess(**post_data)
        aa=self.uu.get_by_email(post_data['user_email'])
        assert aa.uid==self.uid
        self.tearDown()

    def test_set_sendemail_time(self):
        self.add_mess()
        bb= self.uu.get_by_uid(self.uid)

        time.sleep(2)
        self.uu.set_sendemail_time(self.uid)
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
