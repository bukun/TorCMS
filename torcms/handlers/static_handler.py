# -*- coding:utf-8 -*-

'''
All other static pages.
'''

import os
from torcms.core.base_handler import BaseHandler


class StaticHandler(BaseHandler):
    def initialize(self):
        super(StaticHandler, self).initialize()

    def get(self, url_str):
        kwd = {
            'pager': '',
        }
        static_html_file = 'templates/static_pages/{0}'.format(url_str)
        if os.path.exists(static_html_file) and os.path.isfile(static_html_file):
            kwd['info'] = ''
            self.render('static_pages/{0}'.format(url_str),
                        kwd=kwd,
                        userinfo=self.userinfo)
        else:
            kwd['info'] = '404! Page not found.'
            self.render('misc/html/404.html', kwd=kwd,
                        userinfo=self.userinfo)
