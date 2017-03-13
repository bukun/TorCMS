# -*- coding:utf-8 -*-

'''
Handler for wiki, and page.
'''


from .wiki_handler import WikiHandler


class WikiAjaxHandler(WikiHandler):
    def initialize(self):
        super(WikiAjaxHandler, self).initialize()
        self.kind = '1'
