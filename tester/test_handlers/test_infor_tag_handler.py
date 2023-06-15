# # -*- coding:utf-8 -*-

'''
LabelHandler
'''
import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from application import APP


class TestSomeHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_lable(self):
        '''
        Test publish.
        '''
        response = self.fetch('/label/')
        self.assertEqual(response.code, 200)