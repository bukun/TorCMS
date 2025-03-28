# -*- coding:utf-8 -*-
'''
Handler for wiki, and page.
'''

import json
from concurrent.futures import ThreadPoolExecutor

import tornado.escape
import tornado.gen
import tornado.ioloop
import tornado.web

import config
from torcms.core import privilege, tools
from torcms.core.base_handler import BaseHandler
from torcms.model.staff2role_model import MStaff2Role
from torcms.model.wiki_hist_model import MWikiHist
from torcms.model.wiki_model import MWiki

# from celery_server import cele_gen_whoosh


class WikiHandler(BaseHandler):
    '''
    Handler for wiki, and page.
    '''

    executor = ThreadPoolExecutor(2)

    def initialize(self, **kwargs):
        super().initialize()
        self.kind = '1'

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_str in ['', 'recent', '_recent']:
            self.recent()

        elif url_str == 'refresh':
            self.refresh()
        elif url_arr[0] in ['_edit', 'edit']:
            self.to_edit(url_arr[1])
        elif len(url_arr) == 1:
            self.view_or_add(url_str)
        else:
            self.show404()

    def post(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        if url_arr[0] in ['_edit', 'edit']:
            self.update(url_arr[1])
        elif url_arr[0] in ['_add', 'add']:
            self.add()
        elif len(url_arr) == 1:
            self.add(url_str)
        else:
            self.show404()

    def recent(self):
        '''
        List recent wiki.
        '''
        kwd = {
            'pager': '',
            'title': 'Recent Pages',
        }
        self.render(
            'wiki_page/wiki_list.html',
            view=MWiki.query_recent(),
            format_date=tools.format_date,
            kwd=kwd,
            userinfo=self.userinfo,
        )

    def refresh(self):
        '''
        List the wikis of dated.
        '''
        kwd = {
            'pager': '',
            'title': '最近文档',
        }
        self.render(
            'wiki_page/wiki_list.html',
            view=MWiki.query_dated(16),
            format_date=tools.format_date,
            kwd=kwd,
            userinfo=self.userinfo,
        )

    def view_or_add(self, title):
        '''
        To judge if there is a post of the title.
        Then, to show, or to add.
        '''
        postinfo = MWiki.get_by_wiki(title)
        if postinfo:
            if postinfo.kind == self.kind:
                self.view(postinfo)
            else:
                return False
        else:
            self.to_add(title)

    @privilege.permission(action='can_edit')
    # @tornado.web.asynchronous
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def update(self, uid):
        '''
        Update the wiki.
        '''
        postinfo = MWiki.get_by_uid(uid)

        post_data = self.get_request_arguments()
        post_data['user_name'] = self.userinfo.user_name

        cnt_old = tornado.escape.xhtml_unescape(postinfo.cnt_md).strip()
        cnt_new = post_data['cnt_md'].strip()

        if cnt_old == cnt_new:
            pass
        else:
            MWikiHist.create_wiki_history(postinfo, self.userinfo)

        MWiki.update(uid, post_data)

        # cele_gen_whoosh.delay()
        tornado.ioloop.IOLoop.instance().add_callback(self.cele_gen_whoosh)

        self.redirect('/wiki/{0}'.format(tornado.escape.url_escape(post_data['title'])))

    @tornado.web.authenticated
    @privilege.permission(action='can_edit')
    def to_edit(self, id_rec):
        wiki_rec = MWiki.get_by_uid(id_rec)

        kwd = {
            'pager': '',
        }
        self.render(
            'wiki_page/wiki_edit.html',
            kwd=kwd,
            postinfo=wiki_rec,
            userinfo=self.userinfo,
        )

    def view(self, view):
        '''
        View the wiki.
        '''
        kwd = {'pager': ''}
        MWiki.update_view_count(view.uid)
        if self.userinfo:
            kwd['can_review'] = MStaff2Role.check_permissions(
                self.userinfo.uid, 'can_review'
            )
            kwd['can_edit'] = MStaff2Role.check_permissions(
                self.userinfo.uid, 'can_edit'
            )
        self.render(
            'wiki_page/wiki_view.html', postinfo=view, kwd=kwd, userinfo=self.userinfo
        )

    @tornado.web.authenticated
    @privilege.permission(action='can_add')
    def to_add(self, title):
        kwd = {
            'title': title,
            'pager': '',
        }
        if self.userinfo:
            tmpl = 'wiki_page/wiki_add.html'
        else:
            tmpl = 'wiki_page/wiki_login.html'

        self.render(tmpl, kwd=kwd, userinfo=self.userinfo)

    # @tornado.web.asynchronous
    @tornado.web.authenticated
    @privilege.permission(action='can_add')
    @tornado.gen.coroutine
    def add(self, title=''):
        '''
        Add wiki
        '''

        post_data = self.get_request_arguments()

        if title == '':
            pass
        else:
            post_data['title'] = title.strip()

        post_data['user_name'] = self.userinfo.user_name

        if len(post_data['title'].strip()) < 2:
            kwd = {'info': 'Title cannot be less than 2 characters', 'link': '/'}
            self.render('misc/html/404.html', userinfo=self.userinfo, kwd=kwd)

        if MWiki.get_by_wiki(post_data['title']):
            self.redirect('/wiki/{0}'.format(post_data['title']))
        else:
            MWiki.create_wiki(post_data)

            tornado.ioloop.IOLoop.instance().add_callback(self.cele_gen_whoosh)
            # cele_gen_whoosh.delay()

            self.redirect('/wiki/{0}'.format(post_data['title']))
