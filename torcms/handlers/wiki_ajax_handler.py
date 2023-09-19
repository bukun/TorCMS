# -*- coding:utf-8 -*-
'''
Handler for wiki, and page.
'''

from .wiki_handler import WikiHandler


class WikiAjaxHandler(WikiHandler):
    '''
    Handler for wiki, and page.
    '''

    def initialize(self):
        super().initialize()
        self.kind = '1'
