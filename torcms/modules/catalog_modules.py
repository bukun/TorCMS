# -*- coding:utf-8 -*-
'''
For catalog modules.
'''

import tornado.web

from torcms.model.catalog_model import MCatalog
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog


class CatalogMenu(tornado.web.UIModule):
    '''
    Menu for catalog lists.
    '''

    def render(self, *args, **kwargs):
        # kind = kwargs['kind'] if 'kind' in kwargs else '1'
        catid = kwargs['catid'] if 'catid' in kwargs else ''
        recs = MCatalog.query_all()

        return self.render_string(
            'modules/catalog/catalog_list.html', recs=recs, catid=catid
        )


class CatalogList(tornado.web.UIModule):
    '''
    catalog lists.
    '''

    def render(self, *args, **kwargs):
        catid = kwargs['catid'] if 'catid' in kwargs else ''
        cat_id = catid[:2]
        recs = MCategory.get_qian2(cat_id)

        return self.render_string(
            'modules/catalog/catalog_menu.html', recs=recs, catid=catid
        )


class CatalogContent(tornado.web.UIModule):
    ''' '''

    def render(self, *args, **kwargs):
        slug = args[0]

        uid = kwargs.get('uid', False)
        userinfo = kwargs.get('userinfo', None)

        cat_rec = MCategory.get_by_slug(slug)
        if cat_rec:
            cat_id = cat_rec.uid
        else:
            return None
        recs = MPost2Catalog.query_list_by_uid(slug, uid=uid)
        cats = MCategory.query_sub_cat(cat_id, order_uid=True)
        kwd = {
            'slug': slug,
            'userinfo': userinfo,
            'cat_id': cat_id,
            'cats': cats,
        }

        return self.render_string(
            'modules/catalog/catalog_content.html', recs=recs, kwd=kwd
        )
