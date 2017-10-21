# -*- coding:utf-8 -*-

'''
Test user login.
'''


from tornado.testing import AsyncHTTPTestCase
from application import  APP
from http import cookies


TEST_URL = '/resource'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'


class LoginTest(AsyncHTTPTestCase):
    '''
    Test user login.
    '''
    def __init__(self, *rest):
        self.cookies = cookies.SimpleCookie()
        AsyncHTTPTestCase.__init__(self, *rest)

    def get_app(self):
        '''
        Test
        '''
        return APP
