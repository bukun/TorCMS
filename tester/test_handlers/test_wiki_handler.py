# -*- coding:utf-8 -*-


'''
Test Post handler
'''

from tornado.testing import AsyncHTTPSTestCase, gen_test

from application import APP


class TestWikiHandler(AsyncHTTPSTestCase):
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
        response = self.fetch('/wiki/ToAdd')
        # Not log in.
        self.assertEqual(response.code, 200)
    def test_to_recent(self):
        '''
        Test
        '''
        response = self.fetch('/wiki/recent')
        self.assertEqual(response.code, 200)
    def test_to_recent_sec(self):
        '''
        Test
        '''
        response = self.fetch('/wiki/_recent')
        self.assertEqual(response.code, 200)
    def test_to_index(self):
        '''
        Test
        '''
        response = self.fetch('/wiki/')
        self.assertEqual(response.code, 200)
    def test_to_refresh(self):
        '''
        Test
        '''
        response = self.fetch('/wiki/refresh')
        self.assertEqual(response.code, 200)
    def test_to_edit(self):
        '''
        Test
        '''
        response = self.fetch('/wiki/edit/')
        self.assertEqual(response.code, 200)
    def test_to_edit_sec(self):
        '''
        Test
        '''
        response = self.fetch('/wiki/_edit/')
        self.assertEqual(response.code, 200)
