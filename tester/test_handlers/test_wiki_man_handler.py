# -*- coding:utf-8 -*-

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

    def test_to_view(self):
        '''
        Test
        '''
        response = self.fetch('/wiki_man/view/')

        self.assertEqual(response.code, 200)

    def test_to_edit(self):
        '''
        Test
        '''
        response = self.fetch('/wiki_man/edit/')

        self.assertEqual(response.code, 200)

    def test_to_restore(self):
        '''
        Test
        '''
        response = self.fetch('/wiki_man/restore/')

        self.assertEqual(response.code, 200)

    def test_to_delete(self):
        '''
        Test
        '''
        response = self.fetch('/wiki_man/delete/')

        self.assertEqual(response.code, 200)


class TestWikiHistoryHandler(AsyncHTTPSTestCase):
    '''
    Test
    '''

    def get_app(self):
        '''
        Test
        '''
        return APP

    def test_to_view(self):
        '''
        Test
        '''
        response = self.fetch('/page_man/view/')

        self.assertEqual(response.code, 200)

    def test_to_edit(self):
        '''
        Test
        '''
        response = self.fetch('/page_man/edit/')

        self.assertEqual(response.code, 200)

    def test_to_restore(self):
        '''
        Test
        '''
        response = self.fetch('/page_man/restore/')

        self.assertEqual(response.code, 200)

    def test_to_delete(self):
        '''
        Test
        '''
        response = self.fetch('/page_man/delete/')

        self.assertEqual(response.code, 200)
