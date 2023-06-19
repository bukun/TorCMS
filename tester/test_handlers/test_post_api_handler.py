# -*- coding:utf-8 -*-

'''
ApiPostHandler
'''
import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from application import APP

class TestApiPostHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_list(self):
        '''
        Test .
        '''
        response = self.fetch('/api/post/list/')
        self.assertEqual(response.code, 200)

    def test_edit(self):
        '''
        Test .
        '''
        response = self.fetch('/api/post/_edit/')
        self.assertEqual(response.code, 200)
    def test_delete(self):
        '''
        Test .
        '''
        response = self.fetch('/api/post/_delete/')
        self.assertEqual(response.code, 200)

    def test_submit_process(self):
        '''
        Test .
        '''
        response = self.fetch('/api/post/submit_process/')
        self.assertEqual(response.code, 200)
    def test_amis_submit_action(self):
        '''
        Test .
        '''
        response = self.fetch('/api/post/amis_submit_action/')
        self.assertEqual(response.code, 200)
    def test_rovoke(self):
        '''
        Test .
        '''
        response = self.fetch('/api/post/rovoke/')
        self.assertEqual(response.code, 200)