# -*- coding:utf-8 -*-

'''
UserApi
'''
import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from server import APP


class TestProcessHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_chainedOptions(self):
        '''
        Test.
        '''
        response = self.fetch('/api/process/chainedOptions')
        self.assertEqual(response.code, 200)

    def test_list(self):
        '''
        Test.
        '''
        response = self.fetch('/api/process/list/')
        self.assertEqual(response.code, 200)
