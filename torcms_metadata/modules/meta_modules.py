# -*- coding:utf-8 -*-

'''
Define the metadata module for TorCMS.
'''
import config
import tornado.web
from torcms.model.category_model import MCategory
from torcms.model.post_model import MPost
from config import router_post


class Upload_excel(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        uid = args[0]
        router = args[1]
        return self.render_string(
            '../torcms_metadata/tmpl_modules/upload_excel.html',
            uid=uid,
            router=router
        )


class Meta_Recent(tornado.web.UIModule):
    '''
    The reccent posts of certain category.
    '''

    def render(self, *args, **kwargs):

        cat_id = args[0]
        label = kwargs.get('label', None)
        num = kwargs.get('num', 10)
        with_catalog = kwargs.get('with_catalog', True)
        with_date = kwargs.get('with_date', True)
        glyph = kwargs.get('glyph', '')

        is_spa = kwargs.get('spa', False)
        order = kwargs.get('order', False)
        post_uid = kwargs.get('post_uid', '')

        catinfo = MCategory.get_by_uid(cat_id)
        if catinfo.pid == '0000':
            subcats = MCategory.query_sub_cat(cat_id)
            sub_cat_ids = [x.uid for x in subcats]
            recs = MPost.query_total_cat_recent(sub_cat_ids,
                                                label=label,
                                                num=num,
                                                kind=catinfo.kind)

        else:
            recs = MPost.query_cat_recent(cat_id,
                                          label=label,
                                          num=num,
                                          kind=catinfo.kind,
                                          order=order)

        kwd = {
            'with_catalog': with_catalog,
            'with_category': with_catalog,
            'with_date': with_date,
            'router': config.router_post[catinfo.kind],
            'glyph': glyph,
            'spa': is_spa,
            'order': order,
            'kind': catinfo.kind,
            'post_uid': post_uid
        }

        return self.render_string('../torcms_metadata/tmpl_modules/meta_list.html',
                                  recs=recs,
                                  kwd=kwd)


class MetaCategoryOf(tornado.web.UIModule):
    '''
    The catalog of the post.
    '''

    def render(self, uid_with_str, **kwargs):
        curinfo = MCategory.get_by_uid(uid_with_str)
        sub_cats = MCategory.query_sub_cat(uid_with_str)
        kind = kwargs.get('kind', '9')
        cat_dic = []
        for cat in sub_cats:
            res = MPost.query_by_tag(cat.uid, kind)

            if res.count() == 0:
                pass
            else:
                cat_dic.append({cat.uid: cat.name})
        kwd = {
            'glyph': kwargs.get('glyph', ''),
            'order': kwargs.get('order', False),
            'with_title': kwargs.get('with_title', True),
            'router': router_post[kind],
            'kind': kind
        }

        return self.render_string('../torcms_metadata/tmpl_modules/meta_catalog_of.html',
                                  pcatinfo=curinfo,
                                  recs=cat_dic,
                                  kwd=kwd)


# 一二三級分類
class MetaCategory(tornado.web.UIModule):
    '''
    The catalog of the post.
    '''

    def render(self, uid_with_str, **kwargs):
        curinfo = MCategory.get_by_uid(uid_with_str)
        sub_cats = MCategory.query_sub_cat(uid_with_str)
        kind = kwargs.get('kind', '9')
        cur_catid = kwargs.get('catinfo')

        kwd = {
            'glyph': kwargs.get('glyph', ''),
            'order': kwargs.get('order', False),
            'with_title': kwargs.get('with_title', True),
            'cat_id': uid_with_str,
            'accid': kwargs.get('accid', ''),
            'router': router_post[kind],
            'cur_catid': cur_catid
        }

        return self.render_string('../torcms_metadata/tmpl_modules/meta_catalog.html',
                                  pcatinfo=curinfo,
                                  recs=sub_cats,
                                  kwd=kwd)

