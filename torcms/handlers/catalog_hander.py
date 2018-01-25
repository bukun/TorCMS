# -*- coding:utf-8 -*-

'''
For catalog hander.
'''

# from html2text import html2text
#
# from config import CMS_CFG, router_post
# from torcms.core import tools
from torcms.handlers.category_handler import CategoryHandler


# from torcms.model.catalog_model import MCatalog
# from torcms.model.category_model import MCategory
# from torcms.model.post2catalog_model import MPost2Catalog


class CatalogHandler(CategoryHandler):
    '''
    For catalog hander.
    '''

    def initialize(self, **kwargs):
        super(CatalogHandler, self).initialize()
        self.kind = kwargs.get('kind', '1')
        self.order = False

        # def list_catalog(self, cat_slug, **kwargs):
        #     '''
        #     listing the posts via category
        #     '''
        #
        #     post_data = self.get_post_data()
        #     tag = post_data.get('tag', '')
        #
        #     def get_pager_idx():
        #         '''
        #         Get the pager index.
        #         '''
        #         cur_p = kwargs.get('cur_p')
        #         the_num = int(cur_p) if cur_p else 1
        #         the_num = 1 if the_num < 1 else the_num
        #         return the_num
        #
        #     current_page_num = get_pager_idx()
        #     cat_rec = MCategory.get_by_slug(cat_slug)
        #     if not cat_rec:
        #         return False
        #
        #     num_of_cat = MPost2Catalog.count_of_certain_category(cat_rec.uid, tag=tag)
        #
        #     page_num = int(num_of_cat / CMS_CFG['list_num']) + 1
        #     cat_name = cat_rec.name
        #     kwd = {'cat_name': cat_name,
        #            'cat_slug': cat_slug,
        #            'title': cat_name,
        #            'router': router_post[cat_rec.kind],
        #            'current_page': current_page_num,
        #            'kind': cat_rec.kind,
        #            'tag': tag}
        #
        #     tmpl = 'list/catalog_list.html'
        #
        #     self.render(tmpl,
        #                 catinfo=cat_rec,
        #                 infos=MCatalog.query_by_slug(cat_slug),
        #                 pager=tools.gen_pager_purecss(
        #                     '/category/{0}'.format(cat_slug),
        #                     page_num,
        #                     current_page_num),
        #                 userinfo=self.userinfo,
        #                 html2text=html2text,
        #                 cfg=CMS_CFG,
        #                 kwd=kwd,
        #                 router=router_post[cat_rec.kind])
