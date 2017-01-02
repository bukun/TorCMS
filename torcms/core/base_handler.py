# -*- coding:utf-8 -*-

import tornado.web
# from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from torcms.model.user_model import MUser


# Used for jinja2
# class TemplateRendring(object):
#     """
#     A simple class to hold methods for rendering templates.
#     """
#
#     def render_template(self, template_name, **kwargs):
#         template_dirs = []
#         if self.settings.get('template_path', ''):
#             template_dirs.append(self.settings['template_path'])
#         env = Environment(loader=FileSystemLoader(template_dirs))
#
#         try:
#             template = env.get_template(template_name)
#         except TemplateNotFound:
#             raise TemplateNotFound(template_name)
#         content = template.render(kwargs)
#         return content


# class BaseHandler(tornado.web.RequestHandler, TemplateRendring):
class BaseHandler(tornado.web.RequestHandler):
    '''
    The base class for handlers.
    '''

    def initialize(self):
        super(BaseHandler, self).initialize()
        self.muser = MUser()
        if self.get_current_user():
            self.userinfo = self.muser.get_by_name(self.get_current_user())
        else:
            self.userinfo = None

    def get_post_data(self):
        '''
        Get all the arguments from post request.
        Only get the first argument by default.
        :return: post_data.
        '''
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)[0]
        return post_data

    def parse_url(self, url_str):
        '''
        split the url_str to array.
        :param url_str: the request url.
        :return: the array of request url.
        '''
        url_str = url_str.strip()
        return  [] if len(url_str) == 0 else url_str.split('/')

    def check_post_role(self, userinfo):
        '''
        check the user role for docs.
        :param userinfo:
        :return:
        '''
        priv_dic = {'ADD': False, 'EDIT': False, 'DELETE': False, 'ADMIN': False}
        if userinfo:
            pass
        else:
            return priv_dic
        if userinfo.role[1] > '0':
            priv_dic['ADD'] = True
        if userinfo.role[1] >= '1':
            priv_dic['EDIT'] = True
        if userinfo.role[1] >= '3':
            priv_dic['DELETE'] = True
        if userinfo.role[1] >= '2':
            priv_dic['ADMIN'] = True
        return priv_dic

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def is_admin(self):
        if self.check_post_role(self.userinfo)['ADMIN']:
            return True
        else:
            return False

    def editable(self):
        # Deprecated
        if self.check_post_role(self.userinfo)['EDIT']:
            return True
        else:
            return False


    def data_received(self, chunk):
        return False
