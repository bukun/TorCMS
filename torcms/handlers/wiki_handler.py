# -*- coding:utf-8 -*-

import json
import tornado.escape
import tornado.web
from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.wiki_model import MWiki
from torcms.model.wiki_hist_model import MWikiHist


class WikiHandler(BaseHandler):
    def initialize(self):
        super(WikiHandler, self).initialize()
        self.mwiki = MWiki()
        self.mwiki_hist = MWikiHist()
        self.kind = '1'

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)
        if url_str == 'recent':
            self.recent()
        elif url_arr[0] in ['ajax_count_plus', 'j_count_plus']:
            self.j_count_plus(url_arr[1])
        elif url_str == 'refresh':
            self.refresh()
        elif url_arr[0] in ['_edit', 'edit']:
            self.to_edit(url_arr[1])
        elif len(url_arr) == 1:
            self.view_or_add(url_str)
        else:
            kwd = {
                'info': '404 Page not found!',
            }
            self.render('html/404.html', kwd=kwd)

    def post(self, url_str=''):
        url_arr = self.parse_url(url_str)
        if url_arr[0] in ['_edit', 'edit']:
            self.update(url_arr[1])
        elif url_arr[0] in ['_add', 'add']:
            self.add()
        elif len(url_arr) == 1:
            self.add(url_str)
        else:
            kwd = {
                'info': '404 Page not found!',
            }
            self.render('html/404.html', kwd=kwd)

    def recent(self):
        '''
        List recent wiki.
        :return:
        '''
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': 'Recent Pages',
        }
        self.render('doc/wiki/wiki_list.html',
                    view=self.mwiki.query_recent(),
                    format_date=tools.format_date,
                    kwd=kwd,
                    userinfo=self.userinfo,
                    )

    def refresh(self):
        '''
        List the wikis of dated.
        :return:
        '''
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': '最近文档',
        }
        self.render('doc/wiki/wiki_list.html',
                    view=self.mwiki.query_dated(16),
                    format_date=tools.format_date,
                    kwd=kwd,
                    userinfo=self.userinfo,
                    )

    def view_or_add(self, title):
        postinfo = self.mwiki.get_by_wiki(title)
        if postinfo:
            if postinfo.kind == self.kind:
                self.view(postinfo)
            else:
                return False
        else:
            self.to_add(title)

    @tornado.web.authenticated
    def update(self, uid):
        '''
        Update the wiki.
        :param uid:  The ID of the wiki.
        :return:
        '''
        postinfo = self.mwiki.get_by_id(uid)
        if self.check_post_role(self.userinfo)['EDIT'] or postinfo.user_name == self.get_current_user():
            pass
        else:
            return False
        post_data = self.get_post_data()

        post_data['user_name'] = self.get_current_user()

        cnt_old = tornado.escape.xhtml_unescape(postinfo.cnt_md).strip()
        cnt_new = post_data['cnt_md'].strip()

        if cnt_old == cnt_new:
            pass
        else:
            self.mwiki_hist.insert_data(postinfo)

        self.mwiki.update(uid, post_data)

        self.redirect('/wiki/{0}'.format(tornado.escape.url_escape(post_data['title'])))

    @tornado.web.authenticated
    def to_edit(self, id_rec):
        wiki_rec = self.mwiki.get_by_id(id_rec)
        # 用户具有管理权限，或文章是用户自己发布的。
        if self.check_post_role(self.userinfo)['EDIT'] or wiki_rec.user_name == self.get_current_user():
            pass
        else:
            return False

        kwd = {
            'pager': '',
        }
        self.render('doc/wiki/wiki_edit.html',
                    kwd=kwd,
                    unescape=tornado.escape.xhtml_unescape,
                    dbrec=wiki_rec,  # Deprecated.
                    postinfo=wiki_rec,
                    # cfg=cfg, # Todo: Should delete
                    userinfo=self.userinfo,
                    )

    def view(self, view):
        kwd = {
            'pager': '',
            'editable': self.editable(),
        }
        self.render('doc/wiki/wiki_view.html',
                    view=view,  # Deprecated
                    postinfo=view,
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    userinfo=self.userinfo,
                    )

    def j_count_plus(self, slug):
        output = {
            'status': 1 if self.mwiki.update_view_count(slug) else 0,
        }

        return json.dump(output, self)

    def to_add(self, title):
        kwd = {
            'title': title,
            'pager': '',
        }
        if self.userinfo and self.userinfo.role[0] > '0':
            tmpl = 'doc/wiki/wiki_add.html'
        else:
            tmpl = 'doc/wiki/wiki_login.html'

        self.render(tmpl,
                    kwd=kwd,
                    userinfo=self.userinfo,
                    )

    @tornado.web.authenticated
    def add(self, title=''):
        if self.userinfo.role[0] > '0':
            pass
        else:
            return False

        post_data = self.get_post_data()

        if title == '':
            pass
        else:
            post_data['title'] = title
        post_data['user_name'] = self.get_current_user()
        if self.mwiki.get_by_wiki(post_data['title']):
            pass
        else:
            self.mwiki.insert_data(post_data)

        self.redirect('/wiki/{0}'.format(tornado.escape.url_escape(post_data['title'])))
