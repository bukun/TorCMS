# -*- coding:utf-8 -*-
'''
Test
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

    def test_post_man(self):
        '''
        Test view.
        '''
        response = self.fetch('/post_man/view/')
        self.assertEqual(response.code, 200)

    def test_post_man_edit(self):
        '''
        Test edit.
        '''
        response = self.fetch('/post_man/edit/')
        self.assertEqual(response.code, 200)

    def test_post_man_restore(self):
        '''
        Test restore.
        '''
        response = self.fetch('/post_man/restore/')
        self.assertEqual(response.code, 200)

    def test_post_man_delete(self):
        '''
        Test delete.
        '''
        response = self.fetch('/post_man/delete/')
        self.assertEqual(response.code, 200)

    def test_meta_man(self):
        '''
        Test view.
        '''
        response = self.fetch('/meta_man/view/')
        self.assertEqual(response.code, 200)

    def test_meta_man_edit(self):
        '''
        Test edit.
        '''
        response = self.fetch('/meta_man/edit/')
        self.assertEqual(response.code, 200)

    def test_meta_man_restore(self):
        '''
        Test restore.
        '''
        response = self.fetch('/meta_man/restore/')
        self.assertEqual(response.code, 200)

    def test_meta_man_delete(self):
        '''
        Test delete.
        '''
        response = self.fetch('/meta_man/delete/')
        self.assertEqual(response.code, 200)
