# -*- coding:utf-8 -*-

import json
from torcms.handlers.page_handler import PageHandler
from torcms.model.category_model import MCategory
from torcms.model.wiki_model import MWiki


class PageAjaxHandler(PageHandler):
    def initialize(self):
        super(PageAjaxHandler, self).initialize()

    def get(self, *args):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['count_plus']:
            self.j_count_plus(url_arr[1])
        elif url_arr[0] in ['list']:
            self.p_list()
        elif url_arr[0] in ['_add']:
            self.p_to_add()
        else:
            return '{}'

    def j_count_plus(self, slug):
        output = {'status': 1 if MWiki.view_count_plus(slug) else 0}
        return json.dump(output, self)

    def p_list(self):
        pages = MWiki.query_recent(20, kind='2')

        self.render('admin/page_p/page_p_list.html', postrecs=pages)
    def p_to_add(self):
        '''
        To add the page.
        :return:
        '''
        self.render('admin/page_p/page_p_add.html', kwd = {})