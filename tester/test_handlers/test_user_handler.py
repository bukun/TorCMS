# -*- coding:utf-8 -*-

'''
Test user handler
'''

from tornado.testing import AsyncHTTPSTestCase
from tornado.web import Application
from torcms.handlers.user_handler import UserHandler
from application import SETTINGS


class TestUserHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''
    def get_app(self):
        '''
        Test
        '''
        self.app = Application(
            handlers=[("/user/(.*)", UserHandler, dict())],
            **SETTINGS)
        return self.app

    def test_to_add(self):
        '''
        Test
        '''
        response = self.fetch('/user/login')
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
