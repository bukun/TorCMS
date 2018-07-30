# -*- coding:utf-8 -*-

'''
For catalog modules.
'''

import tornado.web
from torcms.model.catalog_model import MCatalog
from torcms.model.category_model import MCategory


class CatalogMenu(tornado.web.UIModule):
    '''
    Menu for catalog lists.
    '''

    def render(self, *args, **kwargs):
        # kind = kwargs['kind'] if 'kind' in kwargs else '1'
        catid = kwargs['catid'] if 'catid' in kwargs else ''
        recs = MCatalog.query_all()

        return self.render_string('modules/catalog/catalog_list.html',
                                  recs=recs,
                                  catid=catid)


class CatalogList(tornado.web.UIModule):
    '''
    catalog lists.
    '''
    def render(self, *args, **kwargs):
        catid = kwargs['catid'] if 'catid' in kwargs else ''
        cat_id = catid[:2]
        recs = MCategory.get_qian2(cat_id)

        return self.render_string('modules/catalog/catalog_menu.html',
                                  recs=recs,
                                  catid=catid)
