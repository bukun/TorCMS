# -*- coding:utf-8 -*-
'''
List infors of the User.
'''

import tornado.web

from torcms.model.post_model import MPost
from torcms.core.base_handler import BaseHandler


class UserListHandler(BaseHandler):
    '''
    List infors of the User.
    '''

    def initialize(self):
        super(UserListHandler, self).initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        dict_get = {
            'recent': self.to_find,
            'app': self.list_app,
            'user_recent': self.user_recent,
            'user_most': self.user_most,
        }
        dict_get.get(url_str, self.show404)()

        # if url_str == 'recent':
        #     self.to_find()
        # if url_str == 'app':
        #     self.list_app()
        # elif url_str == 'user_recent':
        #     self.user_recent()
        # elif url_str == 'user_most':
        #     self.user_most()
        # else:
        #     self.show404()

    def post(self, *args, **kwargs):
        url_str = args[0]
        # if len(url_str) > 0:
        #     ip_arr = url_str.split('/')
        if url_str == 'find':
            self.find()

    def list_app(self):
        '''
        List the apps.
        '''
        kwd = {
            'pager': '',
            'title': '',
        }
        self.render('user/info_list/list_app.html', kwd=kwd,
                    userinfo=self.userinfo, )

    @tornado.web.authenticated
    def user_most(self):
        '''
        User most used.
        '''
        kwd = {
            'pager': '',
            'title': '',
        }
        self.render('user/info_list/user_most.html',
                    kwd=kwd,
                    user_name=self.get_current_user(),
                    userinfo=self.userinfo)

    @tornado.web.authenticated
    def user_recent(self):
        '''
        User used recently.
        '''
        kwd = {
            'pager': '',
            'title': ''
        }
        self.render('user/info_list/user_recent.html',
                    kwd=kwd,
                    user_name=self.get_current_user(),
                    userinfo=self.userinfo)

    def to_find(self):
        '''
        Todo: the name should be changed.
        list the infors.
        '''
        kwd = {'pager': ''}
        self.render('user/info_list/most.html',
                    topmenu='',
                    userinfo=self.userinfo,
                    kwd=kwd)

    def list_recent(self):
        '''
        List the recent.
        '''
        recs = MPost.query_recent(20)
        kwd = {
            'pager': '',
            'title': '',
        }
        self.render('user/info_list/list.html',
                    kwd=kwd,
                    rand_eqs=MPost.query_random(),
                    recs=recs,
                    userinfo=self.userinfo, )

    def find(self):
        '''
        find the infors.
        '''
        keyword = self.get_argument('keyword').strip()

        kwd = {
            'pager': '',
            'title': '查找结果',
        }
        self.render('user/info_list/find_list.html',
                    userinfo=self.userinfo,
                    kwd=kwd,
                    recs=MPost.get_by_keyword(keyword))
