# -*- coding:utf-8 -*-

'''
Test user handler
'''

from tornado.testing import AsyncHTTPSTestCase, gen_test

from application import APP


class TestSearchHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''
    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_to_add(self):
        '''
        Test
        '''
        response = self.fetch('/search/')
        self.assertEqual(response.code, 200)
