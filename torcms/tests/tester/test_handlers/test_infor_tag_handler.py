# # -*- coding:utf-8 -*-

'''
LabelHandler
'''
import sys

sys.path.append('')

from tornado.testing import AsyncHTTPSTestCase

from server import APP


class TestSomeHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_to_remove(self):
        '''
        Test label.
        '''
        response = self.fetch('/label/remove/')
        self.assertEqual(response.code, 200)
