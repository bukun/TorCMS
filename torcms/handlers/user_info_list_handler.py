# -*- coding:utf-8 -*-

import tornado.web
from torcms.model.info_model import MInfor
from torcms.core.base_handler import BaseHandler
from torcms.model.usage_model import MUsage


class UserListHandler(BaseHandler):
    def initialize(self):
        super(UserListHandler, self).initialize()
        self.minfo = MInfor()
        self.musage = MUsage()

    def get(self, url_str=''):
        if url_str == 'recent':
            self.to_find(url_str)
        if url_str == 'app':
            self.list_app()
        elif url_str == 'user_recent':
            self.user_recent()
        elif url_str == 'user_most':
            self.user_most()
        else:
            kwd = {
                'info': '404. Page not found!',
            }
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo, )

    def list_app(self):
        kwd = {
            'pager': '',
            'title': '最近使用的运算应用',
        }
        self.render('user/info_list/list_app.html', kwd=kwd,
                    userinfo=self.userinfo, )

    @tornado.web.authenticated
    def user_most(self):
        kwd = {
            'pager': '',
            'title': '我使用最多的云算应用',
        }
        self.render('user/info_list/user_most.html'.format(input),
                    kwd=kwd,
                    user_name=self.get_current_user(),
                    userinfo=self.userinfo,
                    )

    @tornado.web.authenticated
    def user_recent(self):
        kwd = {
            'pager': '',
            'title': '我最近使用的云算应用'
        }
        self.render('user/info_list/user_recent.html'.format(input),
                    kwd=kwd,
                    user_name=self.get_current_user(),
                    userinfo=self.userinfo,
                    )

    def post(self, input=''):
        if len(input) > 0:
            ip_arr = input.split(r'/')
        if input == 'find':
            self.find()

    def to_find(self, input):
        kwd = {
            'pager': '',
        }
        self.render('user/info_list/most.html'.format(input),
                    topmenu='',
                    userinfo=self.userinfo,
                    kwd=kwd)

    def list_recent(self):
        recs = self.minfo.query_recent(20)
        kwd = {
            'pager': '',
            'title': '最近使用的云算应用',
        }
        self.render('user/info_list/list.html'.format(input), kwd=kwd, rand_eqs=self.get_random(), recs=recs,
                    userinfo=self.userinfo, )

    def find(self):
        keyword = self.get_argument('keyword').strip()

        kwd = {
            'pager': '',
            'title': '查找结果',
        }
        self.render('user/info_list/find_list.html'.format(input),
                    userinfo=self.userinfo,
                    kwd=kwd,
                    recs=self.minfo.get_by_keyword(keyword))

    def get_random(self):
        return self.minfo.query_random()
