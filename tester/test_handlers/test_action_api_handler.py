# -*- coding:utf-8 -*-

'''
ActionHandler
'''
import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from application import APP


class TestActionHandler(AsyncHTTPSTestCase):
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
        response = self.fetch('/api/action/list/')
        self.assertEqual(response.code, 200)

    def test_edit(self):
        '''
        Test .
        '''
        response = self.fetch('/api/action/_edit/')
        self.assertEqual(response.code, 200)

    def test_edit_process(self):
        '''
        Test .
        '''
        response = self.fetch('/api/action/_edit_process/')
        self.assertEqual(response.code, 200)

    def test_edit_per(self):
        '''
        Test .
        '''
        response = self.fetch('/api/action/_edit_per/')
        self.assertEqual(response.code, 200)

    def test_delete(self):
        '''
        Test .
        '''
        response = self.fetch('/api/action/_delete/')
        self.assertEqual(response.code, 200)

    def test_batch_edit(self):
        '''
        Test .
        '''
        response = self.fetch('/api/action/batch_edit/')
        self.assertEqual(response.code, 200)

    def test_batch_delete(self):
        '''
        Test .
        '''
        response = self.fetch('/api/action/batch_delete/')
        self.assertEqual(response.code, 200)

    def test_add(self):
        '''
        Test .
        '''
        response = self.fetch('/api/action/_add/')
        self.assertEqual(response.code, 200)
