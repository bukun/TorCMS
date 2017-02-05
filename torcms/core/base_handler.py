# -*- coding:utf-8 -*-

'''
Basic for handler
'''

import tornado.web
from torcms.model.user_model import MUser


class BaseHandler(tornado.web.RequestHandler):
    '''
    The base class for handlers.
    '''

    def initialize(self):
        super(BaseHandler, self).initialize()
        if self.get_current_user():
            self.userinfo = MUser.get_by_name(self.get_current_user())
        else:
            self.userinfo = None

    def get_post_data(self):
        '''
        Get all the arguments from post request. Only get the first argument by default.
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
        return [] if len(url_str) == 0 else url_str.split('/')

    def check_post_role(self):
        '''
        check the user role for docs.
        :param userinfo:
        :return:
        '''
        priv_dic = {'ADD': False, 'EDIT': False, 'DELETE': False, 'ADMIN': False}
        if self.userinfo:
            if self.userinfo.role[1] > '0':
                priv_dic['ADD'] = True
            if self.userinfo.role[1] >= '1':
                priv_dic['EDIT'] = True
            if self.userinfo.role[1] >= '3':
                priv_dic['DELETE'] = True
            if self.userinfo.role[1] >= '2':
                priv_dic['ADMIN'] = True
        return priv_dic

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def is_admin(self):
        '''
        :return:
        '''
        return True if self.check_post_role()['ADMIN'] else False

    def editable(self):
        '''
        :return:
        '''
        return True if self.check_post_role()['EDIT'] else False

    def data_received(self, chunk):
        return False
