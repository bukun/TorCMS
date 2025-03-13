# -*- coding:utf-8 -*-

'''
TransitionHandler
'''
import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from server import APP


class TestTransitionHandler(AsyncHTTPSTestCase):
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
        response = self.fetch('/api/transition/list/')
        self.assertEqual(response.code, 200)

    #
    # def test_chainedOptions(self):
    #     '''
    #     Test index.
    #     '''
    #     response = self.fetch('/api/transition/chainedOptions/')
    #     self.assertEqual(response.code, 200)
    def test_delete(self):
        '''
        Test .
        '''
        response = self.fetch('/api/transition/_delete/')
        self.assertEqual(response.code, 200)

    def test_add(self):
        '''
        Test .
        '''
        response = self.fetch('/api/transition/_add/')
        self.assertEqual(response.code, 200)

    def test_batch_delete(self):
        '''
        Test .
        '''
        response = self.fetch('/api/transition/batch_delete/')
        self.assertEqual(response.code, 200)
