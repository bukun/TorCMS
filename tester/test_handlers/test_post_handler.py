# -*- coding:utf-8 -*-

'''
Test Post handler PostAjaxHandler
'''

from tornado.testing import AsyncHTTPSTestCase

from application import APP


class TestPostHandler(AsyncHTTPSTestCase):
    def get_app(self):
        '''
        Test
        '''
        return APP 

    def test_post(self):
        '''
        Test post.
        '''
        response = self.fetch('/post/')
        self.assertEqual(response.code, 200)

    def test_to_add(self):
        '''
        Test add.
        '''
        response = self.fetch('/post/_add/')
        self.assertEqual(response.code, 200)

    def test_to_edit(self):
        '''
        Test edit.
        '''
        response = self.fetch('/post/_edit/')
        self.assertEqual(response.code, 200)

    def test_to_delete(self):
        '''
        Test delete.
        '''
        response = self.fetch('/post/_delete/')
        self.assertEqual(response.code, 200)

    def test_to_cat_add(self):
        '''
        Test cat_add.
        '''
        response = self.fetch('/post/_cat_add/')
        self.assertEqual(response.code, 200)

    def test_to_index(self):
        '''
        Test index.
        '''
        response = self.fetch('/post/index')
        self.assertEqual(response.code, 200)

class TestPostAjaxHandler(AsyncHTTPSTestCase):
    def get_app(self):
        '''
        Test
        '''
        return APP


    def test_to_delete(self):
        '''
        Test delete.
        '''
        response = self.fetch('/post_j/_delete/')
        self.assertEqual(response.code, 200)
    def test_to_delete_sec(self):
        '''
        Test delete.
        '''
        response = self.fetch('/post_j/delete/')
        self.assertEqual(response.code, 200)
    # def test_to_recent(self):
    #     '''
    #     Test recent.
    #     '''
    #     response = self.fetch('/post_j/recent/')
    #     self.assertEqual(response.code, 200)
    def test_to_nullify(self):
        '''
        Test nullify.
        '''
        response = self.fetch('/post_j/nullify/')
        self.assertEqual(response.code, 200)
    def test_to_update_valid(self):
        '''
        Test update_valid.
        '''
        response = self.fetch('/post_j/update_valid/')
        self.assertEqual(response.code, 200)