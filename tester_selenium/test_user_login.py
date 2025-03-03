# -*- coding:utf-8 -*-

'''
Test user login.
'''

import unittest

# from application import APP
from http import cookies

from selenium import webdriver
from tornado.testing import AsyncHTTPTestCase

TEST_URL = '/resource'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'


class LoginTest(AsyncHTTPTestCase):
    '''
    Test user login.
    '''

    print(".." * 100)

    def __init__(self, *rest):
        self.cookies = cookies.SimpleCookie()
        AsyncHTTPTestCase.__init__(self, *rest)
        print("p" * 100)

    def get_app(self):
        '''
        Test
        '''
        LoginTest.__init__()

        # return APP

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8888/user/login"
        self.verificationErrors = []
        self.accept_next_alert = True
        print("t" * 100)


if __name__ == '__main__':
    LoginTest.__init__(1, 'kkk')
