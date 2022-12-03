# -*- coding:utf-8 -*-

import os
import tornado.escape
from torcms.core.base_handler import BaseHandler
# from torcms.model.info_model import MInfor
from torcms.model.post_model import MPost
import json


class JavascriptHandler(BaseHandler):
    def initialize(self):
        super(JavascriptHandler, self).initialize()


    def get(self, url_str=''):
        if len(url_str) > 0:
            pass
        else:
            self.redirect('/')
            return
        url_arr = self.parse_url(url_str)
        print(url_arr)
        info_rec = MPost.get_by_uid(url_arr[0])
        html_path = info_rec.extinfo['html_path']
        print(html_path)
        in_cookie_str = url_arr[-1]
        if self.get_cookie('user_pass') == in_cookie_str:
            pass
        else:
            self.redirect('/')
        self.clear_cookie('user_pass')

        # if info_rec.kind == '2':
        #     app_sig = info_rec.uid
        # else:
        app_sig = info_rec.uid[1:]

        jspath = 'jshtml/{0}/{1}_js.html'.format(os.path.split(html_path)[0], app_sig)

        if os.path.exists('templates/{0}'.format(jspath)):
            print('Got it')
            out_dic = {'html': self.render_string(jspath).decode('utf-8')}
            return json.dump(out_dic, self)
            # return self.render_string(jspath).decode('utf-8')
        else:
            print('None')
            return json.dump({}, self)
