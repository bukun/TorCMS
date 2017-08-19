# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.user_model import MUser
import tornado.escape


class TestUser():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uu = MUser()
        self.username = 'namea'

    def test_insert(self):
        post_data = {
            'user_name': self.username,
            'user_pass': 'g131322',
            'user_email': 'name@kljhqq.com',
        }

        tt = self.uu.create_user(post_data)

        assert tt['success'] == True

    def test_insert2(self):
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

    def test_update_info(self):
        post_data = {
            'user_email': 'ssadfs@163.com'
        }
        self.test_insert()
        user_info = self.uu.get_by_name(self.username)
        tt = self.uu.update_info(user_info.uid, post_data['user_email'])
        assert tt['success'] == True

    def test_update_pass(self):
        post_data = {
            'user_pass': 'sdfsdfsdf'
        }
        # tt = self.uu.update_pass(self.username,  post_data['user_pass'])
        # assert tt

    def test_update_privilege(self):
        post_data = {
            'role': '1111'
        }
        tt = self.uu.update_role(self.username, post_data['role'])
        assert tt == True

    def test_upate(self):
        assert True

    def tearDown(self):
        print("function teardown")
        self.uu.delete_by_user_name(self.username)
