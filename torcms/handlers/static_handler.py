# -*- coding:utf-8 -*-


import os
from torcms.core.base_handler import BaseHandler


class StaticHandler(BaseHandler):
    def initialize(self):
        super(StaticHandler, self).initialize()

    def get(self, url_str):
        kwd = {
            'pager': '',
        }
        static_html_file = 'templates/html/{0}'.format(url_str)
        if os.path.exists(static_html_file) and os.path.isfile(static_html_file):
            kwd['info'] = ''
            self.render('html/{0}'.format(url_str),
                        kwd=kwd,
                        userinfo=self.userinfo)
        else:
            kwd['info'] = '您要找的文件不存在！'
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo)
