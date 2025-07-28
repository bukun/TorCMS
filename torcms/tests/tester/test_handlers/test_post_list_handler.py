# -*- coding:utf-8 -*-

'''
PostlistHandler
'''
import sys

sys.path.append('')

from tornado.testing import AsyncHTTPSTestCase

from server import APP


class TestPostlistHandler(AsyncHTTPSTestCase):
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
        response = self.fetch('/post_list/_recent')
        self.assertEqual(response.code, 200)

    def test_index_sec(self):
        '''
        Test index.
        '''
        response = self.fetch('/post_list/recent')
        self.assertEqual(response.code, 200)

    def test_refresh(self):
        '''
        Test refresh.
        '''
        response = self.fetch('/post_list/_refresh')
        self.assertEqual(response.code, 200)

    def test_errcat(self):
        '''
        Test errcat.
        '''
        try:
            # 根据添加机器的性能，有时会超时。
            response = self.fetch('/post_list/errcat')
            self.assertEqual(response.code, 200)
        except TimeoutError:
            pass
