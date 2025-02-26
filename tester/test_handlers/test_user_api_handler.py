# -*- coding:utf-8 -*-

'''
UserApi
'''
import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from application import APP


class TestUserApiHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_logout(self):
        '''
        Test index.
        '''
        response = self.fetch('/api/user/logout')
        self.assertEqual(response.code, 200)

    # def test_reset_passwd(self):
    #     '''
    #     Test index.
    #     '''
    #     response = self.fetch('/api/user/reset-passwd')
    #     self.assertEqual(response.code, 200)
    # def test_list(self):
    #     '''
    #     Test index.
    #     '''
    #     response = self.fetch('/api/user/list')
    #     self.assertEqual(response.code, 200)
