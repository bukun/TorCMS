
import json
from torcms.core.base_handler import BaseHandler

class SysHandler(BaseHandler):


    def initialize(self, **kwargs):
        super(SysHandler, self).initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1:
             self.set_language(url_str)
        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('misc/html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )



    def set_language(self, language):


         if language == 'ZH':
            print("*" * 50)
            print("zh_CN")
            print("*" * 50)
            self.set_cookie('ulocale', 'zh_CN')
            self.set_cookie('blocale', 'zh_CN')

         else:
            print("*" * 50)
            print("en_us")
            print("*" * 50)
            self.set_cookie('ulocale', 'en_US')
            self.set_cookie('blocale', 'en_US')

