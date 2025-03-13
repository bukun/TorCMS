# -*- coding:utf-8 -*-

'''
CheckHandler
'''
import sys

sys.path.append('')

from tornado.testing import AsyncHTTPSTestCase

from server import APP


class TestCheckHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_pend_review(self):
        '''
        Test pend_review.
        '''
        response = self.fetch('/check/pend_review')
        self.assertEqual(response.code, 200)

    def test_publish(self):
        '''
        Test publish.
        '''
        response = self.fetch('/check/publish')
        self.assertEqual(response.code, 200)

    def test_pend_review_sec(self):
        '''
        Test publish.
        '''
        response = self.fetch('/check/pend_review/')
        self.assertEqual(response.code, 200)

    def test_publish_sec(self):
        '''
        Test publish.
        '''
        response = self.fetch('/check/publish/')
        self.assertEqual(response.code, 200)
