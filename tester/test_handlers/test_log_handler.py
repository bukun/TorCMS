# -*- coding:utf-8 -*-

'''
LogHandler
'''

import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from application import APP


class TestLogHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_log(self):
        '''
        Test index.
        '''
        response = self.fetch('/log/')
        self.assertEqual(response.code, 200)
    # def test_to_pageview(self):
    #     '''
    #     Test pageview.
    #     '''
    #     response = self.fetch('/log/pageview')
    #     self.assertEqual(response.code, 200)
    #
    # def test_to_search(self):
    #     '''
    #     Test search.
    #     '''
    #     response = self.fetch('/log/search')
    #     self.assertEqual(response.code, 200)
    def test_to_add(self):
        '''
        Test add.
        '''
        response = self.fetch('/log/_add')
        self.assertEqual(response.code, 200)

class TestLogAjaxHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP
    def test_log_j(self):
        '''
        Test index.
        '''
        response = self.fetch('/log_j/')
        self.assertEqual(response.code, 200)

    def test_log_j_add(self):
        '''
        Test index.
        '''
        response = self.fetch('/log_j/_add')
        self.assertEqual(response.code, 200)