# -*- coding:utf-8 -*-
'''
Test
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
        self.app = Application(handlers=[("/user/(.*)", UserHandler, {})], **SETTINGS)
        return self.app

    def test_to_recent(self):
        '''
        Test
        '''
        response = self.fetch('/user_list/recent')
        self.assertEqual(response.code, 404)

    def test_to_app(self):
        '''
        Test
        '''
        response = self.fetch('/user_list/app')
        self.assertEqual(response.code, 404)

    # def test_to_user_recent(self):
    #     '''
    #     Test
    #     '''
    #     response = self.fetch('/user_list/user_recent')
    #     self.assertEqual(response.code, 200)
    #
    # def test_to_user_most(self):
    #     '''
    #     Test
    #     '''
    #     response = self.fetch('/user_list/user_most')
    #     self.assertEqual(response.code, 200)
