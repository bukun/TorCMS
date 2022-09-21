# -*- coding:utf-8 -*-
'''
For catalog hander.
'''

from torcms.handlers.list_handler import ListHandler


class CatalogHandler(ListHandler):
    '''
    For catalog hander.
    '''

    def initialize(self, **kwargs):
        super().initialize()
        self.kind = kwargs.get('kind', '1')
        self.order = True
