# -*- coding:utf-8 -*-

'''
TestPermissionHandler
'''
import sys

sys.path.append('')

from tornado.testing import AsyncHTTPSTestCase

from server import APP


class TestPermissionHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_getall(self):
        '''
        Test getall.
        '''
        response = self.fetch('/api/permission/getall/')
        self.assertEqual(response.code, 200)
