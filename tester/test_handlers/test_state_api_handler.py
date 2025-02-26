# -*- coding:utf-8 -*-

'''
TestStateHandler
'''
import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from application import APP


class TestStateHandler(AsyncHTTPSTestCase):
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
        response = self.fetch('/api/state/list/')
        self.assertEqual(response.code, 200)

    def test_chainedOptions(self):
        '''
        Test.
        '''
        response = self.fetch('/api/state/chainedOptions/')
        self.assertEqual(response.code, 200)

    def test_edit(self):
        '''
        Test .
        '''
        response = self.fetch('/api/state/_edit/')
        self.assertEqual(response.code, 200)

    def test_edit_per(self):
        '''
        Test .
        '''
        response = self.fetch('/api/state/_edit_per/')
        self.assertEqual(response.code, 200)

    def test_delete(self):
        '''
        Test .
        '''
        response = self.fetch('/api/state/_delete/')
        self.assertEqual(response.code, 200)

    def test_batch_edit(self):
        '''
        Test .
        '''
        response = self.fetch('/api/state/batch_edit/')
        self.assertEqual(response.code, 200)

    def test_batch_delete(self):
        '''
        Test .
        '''
        response = self.fetch('/api/state/batch_delete/')
        self.assertEqual(response.code, 200)

    def test_add(self):
        '''
        Test .
        '''
        response = self.fetch('/api/state/_add/')
        self.assertEqual(response.code, 200)
