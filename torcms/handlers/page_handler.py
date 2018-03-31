# -*- coding:utf-8 -*-

'''
Page ( with unique slug) handler.
'''

import json
from concurrent.futures import ThreadPoolExecutor
import tornado.escape
import tornado.web
import tornado.ioloop

from torcms.core.base_handler import BaseHandler
from torcms.model.category_model import MCategory
from torcms.model.wiki_hist_model import MWikiHist
from torcms.model.wiki_model import MWiki
from torcms.core import tools
from torcms.core import privilege

from config import CMS_CFG


class PageHandler(BaseHandler):
    '''
    Page ( with unique slug) handler.
    '''
    executor = ThreadPoolExecutor(2)

    def initialize(self, **kwargs):
        super(PageHandler, self).initialize()
        self.kind = '2'

    def get(self, *args, **kwargs):

        url_str = args[0]

        url_arr = self.parse_url(url_str)

        if len(url_arr) == 0:
            # self.list()
            self.set_status(400)
            return
        if len(url_arr) == 1 and url_str.endswith('.html'):
            # Deprecated
            self.redirect(url_str.split('.')[0])
        elif url_arr[0] in ['_edit', 'modify', 'edit']:
            self.to_modify(url_arr[1])
        elif url_str == 'list':
            self.list()
        elif url_arr[0] == 'ajax_count_plus':
            self.ajax_count_plus(url_arr[1])
        elif len(url_arr) == 1:
            self.view_or_add(url_str)
        else:
            self.render('misc/html/404.html', userinfo=self.userinfo, kwd={})

    def post(self, *args, **kwargs):
        url_arr = self.parse_url(args[0])

        if url_arr[0] in ['_edit', 'modify', 'edit']:
            self.update(url_arr[1])
        elif len(url_arr) == 1:
            # like:  /page/new_page
            self.add_page(url_arr[0])
        else:
            self.render('misc/html/404.html', userinfo=self.userinfo, kwd={})

    def view_or_add(self, slug):
        '''
        When access with the slug, It will add the page if there is no record in database.
        '''
        rec_page = MWiki.get_by_uid(slug)

        if rec_page:
            if rec_page.kind == self.kind:
                self.view(rec_page)
            else:
                return False
        else:
            self.to_add(slug)

    @tornado.web.authenticated
    @privilege.auth_add
    def to_add(self, citiao):
        '''
        To Add page.
        '''

        kwd = {
            'cats': MCategory.query_all(),
            'slug': citiao,
            'pager': '',
        }
        self.render('wiki_page/page_add.html',
                    kwd=kwd,
                    userinfo=self.userinfo)

    @tornado.web.authenticated
    def __could_edit(self, slug):
        '''
        Test if the user could edit the page.
        '''
        page_rec = MWiki.get_by_uid(slug)
        if not page_rec:
            return False
        if self.check_post_role()['EDIT']:
            return True
        elif page_rec.user_name == self.userinfo.user_name:
            return True
        else:
            return False

    @tornado.web.authenticated
    @privilege.auth_edit
    def update(self, slug):
        '''
        Update the page.
        '''

        post_data = self.get_post_data()

        post_data['user_name'] = self.userinfo.user_name

        pageinfo = MWiki.get_by_uid(slug)

        cnt_old = tornado.escape.xhtml_unescape(pageinfo.cnt_md).strip()
        cnt_new = post_data['cnt_md'].strip()
        if cnt_old == cnt_new:
            pass
        else:
            MWikiHist.create_wiki_history(MWiki.get_by_uid(slug))

        MWiki.update(slug, post_data)
        tornado.ioloop.IOLoop.instance().add_callback(self.cele_gen_whoosh)

        self.redirect('/page/{0}.html'.format(post_data['slug']))

    @tornado.web.authenticated
    @privilege.auth_edit
    def to_modify(self, uid):
        '''
        Try to modify the page.
        '''

        kwd = {
            'pager': '',

        }
        self.render('wiki_page/page_edit.html',
                    view=MWiki.get_by_uid(uid),  # Deprecated
                    postinfo=MWiki.get_by_uid(uid),
                    kwd=kwd,
                    cfg=CMS_CFG,
                    userinfo=self.userinfo)

    @privilege.auth_view
    def view(self, rec):
        '''
        View the page.
        '''
        kwd = {
            'pager': '',
        }
        self.render('wiki_page/page_view.html',
                    view=rec,  # Deprecated
                    postinfo=rec,
                    kwd=kwd,
                    author=rec.user_name,
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    cfg=CMS_CFG)

    def ajax_count_plus(self, slug):
        '''
        post count plus one via ajax.
        '''
        output = {
            'status': 1 if MWiki.view_count_plus(slug) else 0,
        }

        return json.dump(output, self)

    def list(self):
        '''
        View the list of the pages.
        '''
        kwd = {
            'pager': '',
            'title': '单页列表',
        }
        self.render('wiki_page/page_list.html',
                    kwd=kwd,
                    view=MWiki.query_recent(),
                    view_all=MWiki.query_all(),
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    cfg=CMS_CFG)

    @tornado.web.authenticated
    @privilege.auth_add
    def add_page(self, slug):
        '''
        Add new page.
        '''

        post_data = self.get_post_data()

        post_data['user_name'] = self.userinfo.user_name

        if MWiki.get_by_uid(slug):
            self.set_status(400)
            return False
        else:
            MWiki.create_page(slug, post_data)
            tornado.ioloop.IOLoop.instance().add_callback(self.cele_gen_whoosh)
            self.redirect('/page/{0}'.format(slug))
