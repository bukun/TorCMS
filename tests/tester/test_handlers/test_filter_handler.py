# -*- coding:utf-8 -*-

import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from server import APP


class TestFilterHandler(AsyncHTTPSTestCase):
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
        Test index.
        '''
        response = self.fetch('/filter/')
        self.assertEqual(response.code, 200)
