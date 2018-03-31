# -*- coding:utf-8 -*-
'''
Handler of Pages via Ajax.
'''

import json
import tornado.web
import tornado.escape
from torcms.handlers.page_handler import PageHandler
from torcms.model.wiki_model import MWiki


class PageAjaxHandler(PageHandler):
    '''
    Handler of Pages via Ajax.
    '''

    def initialize(self, **kwargs):
        super(PageAjaxHandler, self).initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['count_plus']:
            self.j_count_plus(url_arr[1])
        elif url_arr[0] in ['list']:
            self.p_list()
        elif url_arr[0] in ['_add']:
            self.p_to_add()
        elif len(url_arr) == 1:
            self.view_or_add(url_str)
        else:
            return '{}'

    def view(self, rec):
        '''
        view the post.
        '''
        out_json = {
            'uid': rec.uid,
            'time_update': rec.time_update,
            'title': rec.title,
            'cnt_html': tornado.escape.xhtml_unescape(rec.cnt_html),

        }
        self.write(json.dumps(out_json))

    @tornado.web.authenticated
    def to_add(self, citiao):
        self.write(json.dumps({'code': citiao}))

    def j_count_plus(self, slug):
        '''
        plus count via ajax.
        '''
        output = {'status': 1 if MWiki.view_count_plus(slug) else 0}
        return json.dump(output, self)

    def p_list(self):
        '''
        List the post .
        '''
        self.render('admin/page_ajax/page_list.html', postrecs=MWiki.query_recent(20, kind='2'))

    def p_to_add(self):
        '''
        To add the page.
        '''
        self.render('admin/page_ajax/page_add.html', kwd={})
