# -*- coding:utf-8 -*-

'''
TestRoleHandler
'''
import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from application import APP


class TestRoleHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_role_list(self):
        '''
        Test
        '''
        response = self.fetch('/api/role/list/')
        self.assertEqual(response.code, 200)

    # def test_role_get(self):
    #     '''
    #     Test
    #     '''
    #     response = self.fetch('/api/role/get/')
    #     self.assertEqual(response.code, 200)
    # def test_role_chainedOptions(self):
    #     '''
    #     Test
    #     '''
    #     response = self.fetch('/api/role/chainedOptions/')
    #     self.assertEqual(response.code, 200)

    def test_role_getpid(self):
        '''
        Test
        '''
        response = self.fetch('/api/role/getpid/')
        self.assertEqual(response.code, 200)
