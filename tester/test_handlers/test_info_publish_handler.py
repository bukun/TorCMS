# -*- coding:utf-8 -*-
'''
PublishHandler
'''

import sys

sys.path.append('.')

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

    def test_index(self):
        '''
        Test publish.
        '''
        response = self.fetch('/publish/')
        print(response.code)
        self.assertEqual(response.code, 200)
