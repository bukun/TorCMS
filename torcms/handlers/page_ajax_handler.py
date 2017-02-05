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
            self.count_plus(url_arr[1])
        else:
            return '{}'

    def count_plus(self, slug):
        output = {'status': 1 if MWiki.view_count_plus(slug) else 0}
        return json.dump(output, self)
