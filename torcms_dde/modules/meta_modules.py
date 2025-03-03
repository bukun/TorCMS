# -*- coding:utf-8 -*-

'''
Define the metadata module for TorCMS.
'''
import tornado.web

import config
from config import post_cfg
from torcms.model.category_model import MCategory
from torcms.model.post_model import MPost


class Upload_excel(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        uid = args[0]
        router = args[1]
        return self.render_string(
            '../torcms_dde/tmpl_modules/dde_upload_excel.html', uid=uid, router=router
        )


# 一二三級分類
class MetaCategory(tornado.web.UIModule):
    '''
    The catalog of the post.
    '''

    def render(self, uid_with_str, **kwargs):
        curinfo = MCategory.get_by_uid(uid_with_str)
        sub_cats = MCategory.query_sub_cat(uid_with_str)
        kind = kwargs.get('kind', 'd')
        cur_catid = kwargs.get('catinfo')

        kwd = {
            'glyph': kwargs.get('glyph', ''),
            'order': kwargs.get('order', False),
            'with_title': kwargs.get('with_title', True),
            'cat_id': uid_with_str,
            'accid': kwargs.get('accid', ''),
            'router': post_cfg[kind]['router'],
            'cur_catid': cur_catid,
        }

        return self.render_string(
            '../torcms_dde/tmpl_modules/dde_catalog.html',
            pcatinfo=curinfo,
            recs=sub_cats,
            kwd=kwd,
        )


class StatisticalInfo(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        recs = MPost.get_all('d')
        return self.render_string(
            '../torcms_dde/tmpl_modules/statistical_info.html', recs=recs
        )
