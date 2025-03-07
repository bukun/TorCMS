# -*- coding:utf-8 -*-

'''
LinkHandler LinkPartialHandler
'''
import sys

sys.path.append('.')

from tornado.testing import AsyncHTTPSTestCase

from server import APP


class TestSomeHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_link(self):
        '''
        Test index.
        '''
        response = self.fetch('/link/list')
        self.assertEqual(response.code, 200)

    def test_to_add(self):
        '''
        Test add method.
        '''
        response = self.fetch('/link/add')
        self.assertEqual(response.code, 200)

    def test_to_add_sec(self):
        '''
        Test add method.
        '''
        response = self.fetch('/link/_add')
        self.assertEqual(response.code, 200)

    def test_to_add_thir(self):
        '''
        Test add method.
        '''
        response = self.fetch('/link/add_link')
        self.assertEqual(response.code, 200)

    def test_to_edit(self):
        '''
        Test edit method.
        '''
        response = self.fetch('/link/_edit/')
        self.assertEqual(response.code, 200)

    def test_to_edit_sec(self):
        '''
        Test edit method.
        '''
        response = self.fetch('/link/edit/')
        self.assertEqual(response.code, 200)

    def test_to_edit_thi(self):
        '''
        Test edit method.
        '''
        response = self.fetch('/link/modify/')
        self.assertEqual(response.code, 200)

    def test_to_delete(self):
        '''
        Test delete method.
        '''
        response = self.fetch('/link/delete/')
        self.assertEqual(response.code, 200)

    def test_to_delete_sec(self):
        '''
        Test delete method.
        '''
        response = self.fetch('/link/_delete/')
        self.assertEqual(response.code, 200)

    def test_link_j(self):
        '''
        Test index.
        '''
        response = self.fetch('/link_j/_add')
        self.assertEqual(response.code, 200)
