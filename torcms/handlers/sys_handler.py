'''
To control the cookie for locale.
'''
import json

from torcms.core.base_handler import BaseHandler


class SysHandler(BaseHandler):
    '''
    To control the cookie for locale.
    '''

    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1 and url_arr[0] == 'locale':
            self.get_language()
        else:
            kwd = {
                'info': 'The page not found.',
            }
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

    def post(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1:
            self.set_language(url_str)
        else:
            kwd = {
                'info': 'The page not found.',
            }
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

    def get_language(self):
        '''
        Get the cookie for locale.
        '''
        u_locael = self.get_cookie('ulocale')
        if u_locael:
            return self.get_cookie('ulocale')
        else:
            return 'en_US'

    def set_language(self, language):
        '''
        Set the cookie for locale.
        '''
        if language == 'ZH':
            self.set_cookie('ulocale', 'zh_CN')
            self.set_cookie('blocale', 'zh_CN')
        else:
            self.set_cookie('ulocale', 'en_US')
            self.set_cookie('blocale', 'en_US')
