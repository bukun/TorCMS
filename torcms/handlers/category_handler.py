# -*- coding:utf-8 -*-

'''
Accessing via category. 
'''

import json
import tornado.escape
import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from html2text import html2text

from config import CMS_CFG, router_post


class CategoryHandler(BaseHandler):
    '''
    Category access.    
    If order is True,  list by order. Just like Book.
    Else, list via the category.
    '''

    def initialize(self, **kwargs):
        super(CategoryHandler, self).initialize()
        self.kind = kwargs['kind'] if 'kind' in kwargs else '1'
        self.order = kwargs['order'] if 'order' in kwargs else False

    def get(self, *args, **kwargs):

        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1:
            self.list_catalog(url_str)
        elif len(url_arr) == 2:
            if url_arr[0] == 'j_subcat':
                self.ajax_subcat_arr(url_arr[1])
            elif url_arr[0] == 'j_kindcat':
                self.ajax_kindcat_arr(url_arr[1])
            else:
                self.list_catalog(url_arr[0], cur_p=url_arr[1])
        else:
            self.render('misc/html/404.html')

    def ajax_subcat_arr(self, pid):
        '''
        Get the sub category.
        :param qian2:
        :return:
        '''
        cur_cat = MCategory.query_sub_cat(pid)

        out_arr = {}
        for x in cur_cat:
            out_arr[x.uid] = x.name
        json.dump(out_arr, self)

    def ajax_kindcat_arr(self, kind_sig):
        '''
        Get the sub category.
        :param qian2:
        :return:
        '''
        cur_cat = MCategory.query_kind_cat(kind_sig)

        out_arr = {}
        for x in cur_cat:
            out_arr[x.uid] = x.name
        json.dump(out_arr, self)

    def list_catalog(self, cat_slug, **kwargs):
        '''
        listing the posts via category
        '''

        # tt = self.request.arguments


        post_data = self.get_post_data()

        tag = post_data['tag'] if 'tag' in post_data else ''

        cur_p = kwargs['cur_p'] if 'cur_p' in kwargs else ''

        if cur_p == '':
            current_page_num = 1
        else:
            current_page_num = int(cur_p)

        current_page_num = 1 if current_page_num < 1 else current_page_num

        cat_rec = MCategory.get_by_slug(cat_slug)
        if cat_rec:
            pass
        else:
            return False

        num_of_cat = MPost2Catalog.count_of_certain_category(cat_rec.uid, tag=tag)

        page_num = int(num_of_cat / CMS_CFG['list_num']) + 1
        cat_name = cat_rec.name
        kwd = {'cat_name': cat_name,
               'cat_slug': cat_slug,
               'unescape': tornado.escape.xhtml_unescape,
               'title': cat_name,
               'router': router_post[cat_rec.kind],
               'current_page': current_page_num,
               'kind': cat_rec.kind,
               'tag': tag}

        # tmpl = 'list/catalog_list.html'
        # Todo: review the following codes.

        if self.order:
            tmpl = 'list/catalog_list.html'
        else:
            tmpl = 'list/category_list.html'

        self.render(tmpl,
                    catinfo=cat_rec,
                    infos=MPost2Catalog.query_pager_by_slug(
                        cat_slug,
                        current_page_num,
                        tag=tag,
                        order=self.order, ),
                    pager=tools.gen_pager_purecss(
                        '/category/{0}'.format(cat_slug),
                        page_num,
                        current_page_num),
                    userinfo=self.userinfo,
                    html2text=html2text,
                    unescape=tornado.escape.xhtml_unescape,
                    cfg=CMS_CFG,
                    kwd=kwd,
                    router=router_post[cat_rec.kind])


class TagListHandler(BaseHandler):
    '''
    List the infos by the slug of the catalog.
    via: `/tag/cat_slug`
    '''

    def get(self, *args, **kwargs):
        self.redirect('/category/{0}'.format(args[0]))
