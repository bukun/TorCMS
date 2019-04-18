# -*- coding:utf-8 -*-

'''
Accessing via category.
'''

import json
from html2text import html2text

from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.category_model import MCategory
from torcms.model.catalog_model import MCatalog
from torcms.model.post2catalog_model import MPost2Catalog

from config import CMS_CFG, router_post


class ListHandler(BaseHandler):
    '''
    Category access.
    If order is True,  list by order. Just like Book.
    Else, list via the `category`.


    分类访问
    如果order = True,列表可以进行排序操作。
    '''

    def initialize(self, **kwargs):
        super(ListHandler, self).initialize()
        self.kind = kwargs.get('kind', '1')
        self.order = kwargs.get('order', False)

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
            elif url_arr[0] == 'j_list_catalog':
                self.ajax_list_catalog(url_arr[1])
            else:
                self.list_catalog(url_arr[0], cur_p=url_arr[1])
        else:
            kwd = {
                'title': '',
                'info': '404. Page not found!',
            }
            self.render('misc/html/404.html', kwd=kwd)

    def ajax_list_catalog(self, catid):
        '''
        Get posts of certain catid. In Json.

        根据分类ID（catid）获取 该分类下 post 的相关信息，返回Json格式
        '''
        out_arr = {}
        for catinfo in MPost2Catalog.query_postinfo_by_cat(catid):
            out_arr[catinfo.uid] = catinfo.title

        json.dump(out_arr, self)

    def ajax_subcat_arr(self, pid):
        '''
        Get the sub category.
        ToDo: The menu should display by order. Error fond in DRR.

        根据父类ID（pid）获取子类，返回Json格式
        '''
        out_arr = {}
        for catinfo in MCategory.query_sub_cat(pid):
            out_arr[catinfo.uid] = catinfo.name
        json.dump(out_arr, self)

    def ajax_kindcat_arr(self, kind_sig):
        '''
        Get the sub category.

        根据kind值（kind_sig）获取相应分类，返回Json格式
        '''
        out_arr = {}
        for catinfo in MCategory.query_kind_cat(kind_sig):
            out_arr[catinfo.uid] = catinfo.name
        json.dump(out_arr, self)

    def list_catalog(self, cat_slug, **kwargs):
        '''
        listing the posts via category

        根据分类（cat_slug）显示分类列表
        '''
        post_data = self.get_post_data()
        tag = post_data.get('tag', '')

        def get_pager_idx():
            '''
            Get the pager index.
            '''
            cur_p = kwargs.get('cur_p')
            the_num = int(cur_p) if cur_p else 1
            the_num = 1 if the_num < 1 else the_num
            return the_num

        current_page_num = get_pager_idx()
        cat_rec = MCategory.get_by_slug(cat_slug)
        if not cat_rec:
            return False

        num_of_cat = MPost2Catalog.count_of_certain_category(cat_rec.uid, tag=tag)

        page_num = int(num_of_cat / CMS_CFG['list_num']) + 1
        cat_name = cat_rec.name
        kwd = {'cat_name': cat_name,
               'cat_slug': cat_slug,
               'title': cat_name,
               'router': router_post[cat_rec.kind],
               'current_page': current_page_num,
               'kind': cat_rec.kind,
               'tag': tag}


        # Todo: review the following codes.


        if self.order:
            tmpl = 'list/catalog_list.html'
        else:
            tmpl = 'list/category_list.html'

        infos = MPost2Catalog.query_pager_by_slug(
            cat_slug,
            current_page_num,
            tag=tag,
            order=self.order
        )

        # ToDo: `gen_pager_purecss` should not use any more.
        self.render(tmpl,
                    catinfo=cat_rec,
                    infos=infos,
                    pager=tools.gen_pager_purecss(
                        '/list/{0}'.format(cat_slug),
                        page_num,
                        current_page_num),
                    userinfo=self.userinfo,
                    html2text=html2text,
                    cfg=CMS_CFG,
                    kwd=kwd,
                    router=router_post[cat_rec.kind])


class TagListHandler(BaseHandler):
    '''
    List the infos by the slug of the catalog.
    via: `/tag/cat_slug`
    '''

    def get(self, *args, **kwargs):
        self.redirect('/list/{0}'.format(args[0]))
