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
        return self.render_string('modules/category/showcat_list.html',
                                  recs=MCategory.query_all(kind=kind))


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
        kwd = {'glyph': glyph, 'catid': catid, 'kind': kind}

        return self.render_string('modules/category/showcat_list_second.html',
                                  recs=recs,
                                  catid=catid,
                                  userinfo=userinfo,
                                  kwd=kwd)


class SecondaryCategoryList(tornado.web.UIModule):
    '''
    Secondary Category List
    '''
    def render(self, *args, **kwargs):
        catid = kwargs.get('catid', '')
        second = kwargs.get('second', True)
        userinfo = kwargs.get('userinfo', None)
        post_uid = kwargs.get('post_uid', '')

        glyph = kwargs.get('glyph', '')
        cat_id = catid[:2]
        recs = MCategory.get_qian2(cat_id)
        kwd = {'glyph': glyph, 'catid': catid, 'cat_id': cat_id}
        if second is False:
            return self.render_string('modules/category/showsubcat_list.html',
                                      recs=recs,
                                      catid=catid,
                                      userinfo=userinfo,
                                      kwd=kwd)
        else:
            return self.render_string(
                'modules/category/showsubcat_list_second.html',
                recs=recs,
                catid=catid,
                post_uid=post_uid,
                userinfo=userinfo,
                kwd=kwd)


class CategoryName(tornado.web.UIModule):
    '''

    '''
    def render(self, *args, **kwargs):
        cat_id = args[0]
        order = kwargs.get('order', False)
        if cat_id != '0000':
            catinfo = MCategory.get_by_uid(cat_id)
        else:
            catinfo = ''
        if order:
            cat_url = 'catalog'
        else:
            cat_url = 'list'
        kwd = {'cat_url': cat_url}
        return self.render_string('modules/category/category_name.html',
                                  recs=catinfo,
                                  kwd=kwd)
