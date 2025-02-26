# -*- coding:utf-8 -*-

'''
CommentHandler
'''
import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from application import APP


class TestCommentHandler(AsyncHTTPSTestCase):
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
        response = self.fetch('/comment/')
        self.assertEqual(response.code, 200)

    def test_index_sec(self):
        '''
        Test index.
        '''
        response = self.fetch('/comment/list')
        self.assertEqual(response.code, 200)

    def test_index_cur(self):
        '''
        Test index.
        '''
        response = self.fetch('/comment/list/2')
        self.assertEqual(response.code, 200)
