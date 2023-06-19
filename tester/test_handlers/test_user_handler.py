# -*- coding:utf-8 -*-

'''
Test user handler
'''

from tornado.testing import AsyncHTTPSTestCase
from tornado.web import Application

from application import SETTINGS
from torcms.handlers.user_handler import UserHandler


class TestUserHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        self.app = Application(
            handlers=[("/user/(.*)", UserHandler, {})],
            **SETTINGS)
        return self.app

    def test_to_login(self):
        '''
        Test
        '''
        response = self.fetch('/user/login')
        self.assertEqual(response.code, 200)

    def test_to_regist(self):
        '''
        Test
        '''
        response = self.fetch('/user/regist')
        self.assertEqual(response.code, 200)
        # def test_user_profile_annoymouse(self):
        #     userinfo = MUser.get_by_name('giser')
        #     with mock.patch.object(UserHandler, 'get_secure_cookie') as m:
        #
        #         print('-|' * 20)
        #         print(userinfo)
        #         print(userinfo.uid)
        #         m.return_value = userinfo
        #         reponse = self.fetch('/user/info', method = 'GET')
        #     self.assertEqual('sucess', reponse.body )
    def test_to_info(self):
        '''
        Test
        '''
        response = self.fetch('/user/info')
        self.assertEqual(response.code, 200)

    def test_to_j_regist(self):
        '''
        Test
        '''
        response = self.fetch('/user/j_regist')
        self.assertEqual(response.code, 200)

    def test_to_logout(self):
        '''
        Test
        '''
        response = self.fetch('/user/logout')
        self.assertEqual(response.code, 200)
    def test_to_reset_password(self):
        '''
        Test
        '''
        response = self.fetch('/user/reset-password')
        self.assertEqual(response.code, 200)

    def test_to_changepass(self):
        '''
        Test
        '''
        response = self.fetch('/user/changepass')
        self.assertEqual(response.code, 200)
    def test_to_changeinfo(self):
        '''
        Test
        '''
        response = self.fetch('/user/changeinfo')
        self.assertEqual(response.code, 200)
    # def test_to_reset_passwd(self):
    #     '''
    #     Test
    #     '''
    #     response = self.fetch('/user/reset-passwd')
    #     self.assertEqual(response.code, 200)

    def test_to_changerole(self):
        '''
        Test
        '''
        response = self.fetch('/user/changerole')
        self.assertEqual(response.code, 200)

    def test_to_find(self):
        '''
        Test
        '''
        response = self.fetch('/user/find')
        self.assertEqual(response.code, 200)

    def test_to_delete_user(self):
        '''
        Test
        '''
        response = self.fetch('/user/delete_user/')
        self.assertEqual(response.code, 200)

    def test_to_list(self):
        '''
        Test
        '''
        response = self.fetch('/user/list')
        self.assertEqual(response.code, 200)
    def test_to_pass_strength(self):
        '''
        Test
        '''
        response = self.fetch('/user/pass_strength/')
        self.assertEqual(response.code, 200)