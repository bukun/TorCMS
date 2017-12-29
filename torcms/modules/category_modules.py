# -*- coding:utf-8 -*-

'''
Menu for category lists.
'''

import tornado.web

from torcms.model.category_model import MCategory


class CategoryMenu(tornado.web.UIModule):
    '''
    Menu for category lists.
    '''

    def render(self, *args, **kwargs):
        kind = kwargs['kind'] if 'kind' in kwargs else '1'
        return self.render_string(
            'modules/category/showcat_list.html',
            recs=MCategory.query_all(kind=kind)
        )
