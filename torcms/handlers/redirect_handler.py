# # -*- coding:utf-8 -*-
# import os
#
# from torcms.core.base_handler import BaseHandler
#
#
# class RedirectHandler(BaseHandler):
#     def initialize(self):
#         super(RedirectHandler, self).initialize()
#
#     def get(self, url_str):
#         kwd = {
#             'pager': '',
#         }
#
#         if url_str == 'app' or url_str == 'map':
#             self.redirect('/{0}/'.format(url_str))
#             return True
#         static_html_file = 'templates/html/{0}'.format(url_str)
#
#         if os.path.exists(static_html_file) and os.path.isfile(static_html_file):
#             kwd['pager'] = ''
#             self.render('html/{0}'.format(url_str),
#                         userinfo=self.userinfo,
#                         kwd=kwd)
#         else:
#             kwd['info'] = '您要找的文件不存在！'
#             self.render('html/404.html',
#                         userinfo=self.userinfo,
#                         kwd=kwd)
