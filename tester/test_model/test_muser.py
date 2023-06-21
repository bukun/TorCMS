# -*- coding:utf-8 -*-

import random
import time

import tornado.escape

from torcms.core import tools
from torcms.model.user_model import MUser


class TestMUser():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uu = MUser()
        self.username = 'namea'
        self.username2 = 'test1'
        self.uid = ''
        self.add_mess()

    def test_create_user(self):
        post_data = {
            'user_name': self.username,
            'user_pass': 'Lg131322',
            'user_email': 'name@kljhqq.com',
        }

        tt = self.uu.create_user(post_data)

        assert tt['success'] == False
        assert tt['code'] == '91'

    def add_mess(self, **kwargs):
        name = kwargs.get('user_name', self.username)
        post_data = {
            'user_name': name,
            'user_pass': kwargs.get('user_pass', 'Lg131322'),
            'user_email': kwargs.get('user_email', '{}@kljhqq.com'.format(random.randint(1, 1000000))),
        }

        self.uu.create_user(post_data)
        aa = self.uu.get_by_name(name)
        self.uid = aa.uid

    def test_create_user2(self):
        post_data = {
            'user_name': '',
            'user_pass': 'Lg131322',
            'user_email': 'name@qkjhlq.com',
        }

        tt = self.uu.create_user(post_data)
        assert tt['success'] == False
        assert tt['code'] == '11'

        post_data = {
            'user_name': '天',
            'user_pass': 'Lg131322',
            'user_email': 'name@qhjq.com',
        }

        tt = self.uu.create_user(post_data)
        assert tt['success'] == False
        assert tt['code'] == '11'

        post_data = {
            'user_name': '/sdfadf',
            'user_pass': 'Lg131322',
            'user_email': 'name@qjhgq.com',
        }

        tt = self.uu.create_user(post_data)
        assert tt['success'] == False
        assert tt['code'] == '11'

        post_data = {
            'user_name': 'asddsad',
            'user_pass': 'fg131322',
            'user_email': 'name@qjhgq.com',
        }

        tt = self.uu.create_user(post_data)
        assert tt['success'] == False
        assert tt['code'] == '31'

        post_data = {
            'user_name': 'sdfadf',
            'user_pass': 'Dfg131322',
            'user_email': 'name',
        }

        tt = self.uu.create_user(post_data)
        assert tt['success'] == False
        assert tt['code'] == '21'

    def test_update_info(self):
        post_data = {
            'user_email': 'ssadfs@163.com'
        }

        user_info = self.uu.get_by_name(self.username)
        tt = self.uu.update_info(user_info.uid, post_data['user_email'])
        assert tt['success'] == True

    def test_update_pass(self):

        post_data = {
            'user_pass': 'sdfsdfsdf15G'
        }
        self.uu.update_pass(self.uid, post_data['user_pass'])
        tt = self.uu.get_by_uid(self.uid)
        assert tt.user_pass == tools.md5(post_data['user_pass'])

    def test_update_role(self):

        post_data = {
            'role': '1111',
            'authority': '1'
        }
        self.uu.update_role(self.username, post_data)
        tt = self.uu.get_by_uid(self.uid)
        assert tt.role == post_data['role']

    def test_total_number(self):
        a = self.uu.total_number()

        assert a >= 1

    def test_query_pager_by_slug(self):

        a = self.uu.total_number()
        x = int(a / 10)
        tf = False
        for i in range(x + 2):

            aa = self.uu.query_pager_by_slug(current_page_num=i)
            for y in aa:
                if y.uid == self.uid:
                    tf = True

        assert tf

    def test_count_of_certain(self):
        a = self.uu.count_of_certain()

        assert a >= 1

    #
    # def test_delete(self):
    #     user_info = self.uu.get_by_name(self.username)
    #     self.add_mess()
    #     user_info2 = self.uu.get_by_name(self.username)
    #     aa = self.uu.delete(self.uid)
    #     user_info3 = self.uu.get_by_name(self.username)
    #     assert aa == True
    #     assert user_info == user_info3
    #     assert user_info == None
    #     assert user_info2.uid == self.uid
    #
    # def test_delete_by_user_name(self):
    #     user_info = self.uu.get_by_name(self.username)
    #     self.add_mess()
    #     user_info2 = self.uu.get_by_name(self.username)
    #     aa = self.uu.delete_by_user_name(self.username)
    #     user_info3 = self.uu.get_by_name(self.username)
    #     assert aa == True
    #     assert user_info == user_info3
    #     assert user_info == None
    #     assert user_info2.uid == self.uid

    def test_get_by_keyword(self):

        aa = self.uu.get_by_keyword('me')
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True

        assert tf

    def test_update_time_login(self):

        user_info = self.uu.get_by_name(self.username)
        time.sleep(2)
        self.uu.update_success_info(self.username)
        aa = self.uu.get_by_name(self.username)
        assert user_info.time_login != aa.time_login

    def test_update_time_reset_passwd(self):

        time_r = 11111111
        aa = self.uu.update_time_reset_passwd(self.username, time_r)
        assert aa == True
        aa = self.uu.get_by_name(self.username)
        assert aa.time_reset_passwd == time_r

    def test_check_user_by_email(self):
        post_data = {
            'user_name': self.username2,
            'user_email': 'ssadfs@163.com',
            'user_pass': 'LG1ffffff'
        }
        self.add_mess(**post_data)
        u_name = self.uu.get_by_email(post_data['user_email']).user_name
        aa = self.uu.check_user_by_name(u_name, post_data['user_pass'])
        assert aa == 1

    def test_check_user_by_name(self):
        post_data = {
            'user_pass': 'LG1ffffff'
        }
        self.add_mess(**post_data)
        aa = self.uu.check_user_by_name(self.username, post_data['user_pass'])
        assert aa == 0

    def test_check_user(self):
        post_data = {
            'user_pass': 'LG1ffffff'
        }
        self.add_mess(**post_data)
        aa = self.uu.check_user(self.uid, post_data['user_pass'])
        assert aa == 0

    def test_get_by_email(self):
        post_data = {
            'user_email': 'ssadfs@163.com',
            'user_name': self.username2
        }
        self.add_mess(**post_data)
        aa = self.uu.get_by_email(post_data['user_email'])
        assert aa.uid == self.uid

    def test_set_sendemail_time(self):

        bb = self.uu.get_by_uid(self.uid)

        time.sleep(2)
        self.uu.set_sendemail_time(self.uid)
        aa = self.uu.get_by_uid(self.uid)
        assert bb.time_email <= aa.time_email

    def test_get_by_name(self):

        aa = self.uu.get_by_name(self.username)
        assert aa.uid == self.uid

    def test_get_by_uid(self):

        aa = self.uu.get_by_uid(self.uid)
        assert aa.user_name == self.username

    def test_query_all_1(self):
        aa = self.uu.query_all()
        tf = False
        for i in aa:
            if i.user_name == self.username:
                tf = True
        assert tf

    def test_query_all(self):

        aa = self.uu.query_all()
        tf = False
        for i in aa:
            if i.user_name == self.username:
                tf = True
        assert tf

    def test_db_email(self):

        pdata = {
            'user_name': 'asdfdsf',
            'user_pass': 'LG1sadf',
            'user_email': 'sadflsdf@11.com',
        }
        MUser.create_user(pdata)
        bb = MUser.create_user(pdata)
        bb.pop('uid')
        assert bb == {'code': '31', 'success': False}
        self.uu.delete_by_user_name(pdata['user_name'])

    def teardown_method(self):
        print("function teardown")
        tt = self.uu.get_by_uid(self.uid)
        if tt:
            self.uu.delete(tt.uid)
        self.uu.delete_by_user_name(self.username)
        self.uu.delete_by_user_name(self.username2)
