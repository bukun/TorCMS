# -*- coding:utf-8 -*-
'''
Test
'''
from tornado.testing import AsyncHTTPSTestCase

from server import APP


class TestReplyHandler(AsyncHTTPSTestCase):
    def get_app(self):
        '''
        Test
        '''
        return APP

    # def test_reply_get(self):
    #     '''
    #     Test reply get.
    #     '''
    #     response = self.fetch('/reply/get/')
    #     self.assertEqual(response.code, 200)

    # def test_reply_more(self):
    #     '''
    #     Test reply more.
    #     '''
    #     response = self.fetch('/reply/more/')
    #     self.assertEqual(response.code, 200)
    def test_reply_list(self):
        '''
        Test reply list.
        '''
        response = self.fetch('/reply/list/')
        self.assertEqual(response.code, 200)

    def test_reply_delete(self):
        '''
        Test reply delete.
        '''
        response = self.fetch('/reply/delete/')
        self.assertEqual(response.code, 200)

    def test_reply_delete_com(self):
        '''
        Test reply delete_com.
        '''
        response = self.fetch('/reply/delete_com/')
        self.assertEqual(response.code, 200)

    # def test_reply_zan(self):
    #     '''
    #     Test reply zan.
    #     '''
    #     response = self.fetch('/reply/zan/')
    #     self.assertEqual(response.code, 200)
    def test_reply_count(self):
        '''
        Test reply count.
        '''
        response = self.fetch('/reply/count/')
        self.assertEqual(response.code, 200)

    def test_reply_com_count(self):
        '''
        Test reply com_count.
        '''
        response = self.fetch('/reply/com_count/')
        self.assertEqual(response.code, 200)

    def test_reply_add(self):
        '''
        Test reply com_count.
        '''
        response = self.fetch('/reply/com_count/')
        self.assertEqual(response.code, 200)

    # def test_reply_get_by_user(self):
    #     '''
    #     Test reply get_by_user.
    #     '''
    #     response = self.fetch('/reply/get_by_user/')
    #     self.assertEqual(response.code, 200)


class TestReplyajaxHandler(AsyncHTTPSTestCase):
    def get_app(self):
        '''
        Test
        '''
        return APP

    # def test_reply_get(self):
    #     '''
    #     Test reply get.
    #     '''
    #     response = self.fetch('/reply/get/')
    #     self.assertEqual(response.code, 200)

    # def test_reply_more(self):
    #     '''
    #     Test reply more.
    #     '''
    #     response = self.fetch('/reply/more/')
    #     self.assertEqual(response.code, 200)
    def test_reply_list(self):
        '''
        Test reply list.
        '''
        response = self.fetch('/reply_j/list/')
        self.assertEqual(response.code, 200)

    def test_reply_delete(self):
        '''
        Test reply delete.
        '''
        response = self.fetch('/reply_j/delete/')
        self.assertEqual(response.code, 200)

    def test_reply_delete_com(self):
        '''
        Test reply delete_com.
        '''
        response = self.fetch('/reply_j/delete_com/')
        self.assertEqual(response.code, 200)

    # def test_reply_zan(self):
    #     '''
    #     Test reply zan.
    #     '''
    #     response = self.fetch('/reply/zan/')
    #     self.assertEqual(response.code, 200)
    def test_reply_count(self):
        '''
        Test reply count.
        '''
        response = self.fetch('/reply_j/count/')
        self.assertEqual(response.code, 200)

    def test_reply_com_count(self):
        '''
        Test reply com_count.
        '''
        response = self.fetch('/reply_j/com_count/')
        self.assertEqual(response.code, 200)

    def test_reply_add(self):
        '''
        Test reply com_count.
        '''
        response = self.fetch('/reply_j/com_count/')
        self.assertEqual(response.code, 200)
