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
        kind = kwargs.get('kind', '1')
        return self.render_string(
            'modules/category/showcat_list.html',
            recs=MCategory.query_all(kind=kind)
        )


class SecondaryCategoryMenu(tornado.web.UIModule):
    '''
    Secondary Category Menu
    '''

    def render(self, *args, **kwargs):
        kind = kwargs.get('kind', '1')
        catid = kwargs.get('catid', '')
        userinfo = kwargs.get('userinfo', None)
        glyph = kwargs.get('glyph', '')
        recs = MCategory.get_parent_list(kind=kind)
        kwd = {
            'glyph': glyph,
            'catid': catid,
            'kind': kind

        }

        return self.render_string(
            'modules/category/showcat_list_second.html',
            recs=recs,
            catid=catid,
            userinfo=userinfo,
            kwd=kwd
        )


class SecondaryCategoryList(tornado.web.UIModule):
    '''
    Secondary Category List
    '''

    def render(self, *args, **kwargs):
        catid = kwargs.get('catid', '')
        second = kwargs.get('second', True)
        userinfo = kwargs.get('userinfo', None)

        glyph = kwargs.get('glyph', '')
        cat_id = catid[:2]
        recs = MCategory.get_qian2(cat_id)
        kwd = {
            'glyph': glyph,
            'catid': catid,
            'cat_id': cat_id

        }
        if second == False:
            return self.render_string(
                'modules/category/showsubcat_list.html',
                recs=recs,
                catid=catid,
                userinfo=userinfo,
                kwd=kwd
            )
        else:
            return self.render_string(
                'modules/category/showsubcat_list_second.html',
                recs=recs,
                catid=catid,
                userinfo=userinfo,
                kwd=kwd
            )
