# -*- coding:utf-8 -*-


from torcms.handlers.post_handler import PostHandler

# from tornado.testing import AsyncHTTPSTestCase
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from application import SETTINGS, app
from http import cookies
import urllib
import tornado.escape

TEST_URL = '/resource'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'


class LoginTest(AsyncHTTPTestCase):
    def __init__(self, *rest):
        self.cookies = cookies.SimpleCookie()
        AsyncHTTPTestCase.__init__(self, *rest)

    def get_app(self):
        return app
