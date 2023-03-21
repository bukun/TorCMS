# -*- coding:utf-8 -*-

'''
更新数据分类
'''
import tornado.web
from torcms.core.base_handler import BaseHandler
from torcms.model.post_model import MPost
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.category_model import MCategory
from torcms.core import privilege


class UpdateCategoryHandler(BaseHandler):
    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_str == '' or url_str == 'index':
            self.index()
        elif len(url_arr) == 2:
            if url_arr[0] == 'delete':
                self.del_category(url_arr[1])
        else:
            kwd = {
                'info': 'The Page not Found.',
            }
            self.show404(kwd=kwd)

    def post(self, *args, **kwargs):
        url_arr = self.parse_url(args[0])

        if len(url_arr) == 0:
            # like:  /page/new_page
            self.update_category()

        else:
            self.render('misc/html/404.html', userinfo=self.userinfo, kwd={})

    def index(self):

        self.render('../torcms_taginfo/update_category.html',
                    userinfo=self.userinfo,
                    kwd={})

    @tornado.web.authenticated
    @privilege.permission(action='can_add')
    def del_category(self, uid):
        '''
        Add new page.
        '''

        MCategory.delete(uid)
        self.redirect('/')

    @tornado.web.authenticated
    @privilege.permission(action='can_add')
    def update_category(self):
        '''
        Add new page.
        '''

        post_data = self.get_request_arguments()

        old_catid = post_data['old_catid'].strip()
        new_catid = post_data['new_catid'].strip()
        recs = MPost.query_by_extinfo('def_cat_uid', old_catid)
        extinfo = {}
        for rec in recs:
            extinfo['def_cat_uid'] = new_catid
            extinfo['gcat0'] = new_catid

            mpost2 = MCategory.get_by_info(rec.uid, old_catid)
            MPost2Catalog.update_field(mpost2.uid, tag_id=new_catid)
            MPost.update_jsonb(rec.uid, extinfo)

        MCategory.update_count(old_catid)
        MCategory.update_count(new_catid)

        self.redirect('/filter/{0}'.format(new_catid))
