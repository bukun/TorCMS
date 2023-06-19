# -*- coding:utf-8 -*-

'''
PermissionHandler
'''
import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from application import APP


class TestPermissionHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP

    # def test_index(self):
    #     '''
    #     Test index.
    #     '''
    #     response = self.fetch('/permission/list')
    #     self.assertEqual(response.code, 200)
    #
    # def test_to_get(self):
    #     '''
    #     Test index.
    #     '''
    #     response = self.fetch('/permission/get/')
    #     self.assertEqual(response.code, 200)
    def test_getall(self):
        '''
        Test getall.
        '''
        response = self.fetch('/permission/getall/')
        self.assertEqual(response.code, 200)