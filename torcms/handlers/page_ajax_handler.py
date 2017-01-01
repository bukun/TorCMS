# -*- coding:utf-8 -*-

import json
from torcms.handlers.page_handler import PageHandler
from torcms.model.category_model import MCategory
from torcms.model.page_model import MPage


class PageAjaxHandler(PageHandler):
    def initialize(self):
        super(PageAjaxHandler, self).initialize()
        self.mpage = MPage()
        self.mcat = MCategory()
        self.cats = self.mcat.query_all()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['count_plus']:
            self.count_plus(url_arr[1])
        else:
            return '{}'

    def count_plus(self, slug):
        output = {
            'status': 1 if self.mpage.view_count_plus(slug) else 0,
        }

        return json.dump(output, self)
