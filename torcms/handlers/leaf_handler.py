# -*- coding:utf-8 -*-

'''
The basic  leaf handler.
'''

import random
import tornado.escape
import tornado.web
import tornado.ioloop

from torcms.core.tools import logger
from torcms.model.category_model import MCategory
from torcms.model.label_model import MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
from torcms.model.evaluation_model import MEvaluation
from torcms.model.usage_model import MUsage
from .post_handler import PostHandler
from config import router_post, DB_CFG


class LeafHandler(PostHandler):
    '''
    The basic HTML Page handler.
    '''

    def initialize(self, **kwargs):
        super(LeafHandler, self).initialize()

        if 'kind' in kwargs:
            self.kind = kwargs['kind']
        else:
            self.kind = '1'

        self.filter_view = kwargs['filter_view'] if 'filter_view' in kwargs else False

    def get(self, *args):

        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1 and len(url_str) in [4, 5]:
            self.view_or_add(url_str)
        else:
            kwd = {
                'title': '',
                'info': '404. Page not found!',
            }
            self.set_status(404)
            self.render('misc/html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )

    def post(self, *args):

        url_str = args[0]
        print(url_str)
        url_arr = self.parse_url(url_str)
        if url_arr[0] == 'update_order':
            self.update_order(url_arr[1], url_arr[2])

    @tornado.web.authenticated
    def update_order(self, uid, order):
        if self.userinfo.role[1] > '0':
            MPost.update_order(uid, order)

    def viewinfo(self, postinfo):
        '''
        In infor.
        :param postinfo:
        :return:
        '''
        logger.warning('info kind:{0} '.format(postinfo.kind))

        # If not, there must be something wrong.
        if postinfo.kind == self.kind:
            pass
        else:
            self.redirect('/{0}/{1}'.format(router_post[postinfo.kind], postinfo.uid),
                          permanent=True)

        ######################################################
        if DB_CFG['kind'] == 's':
            cat_enum1 = []

        else:
            ext_catid = postinfo.extinfo['def_cat_uid'] if 'def_cat_uid' in postinfo.extinfo else ''
            ext_catid2 = postinfo.extinfo['def_cat_uid'] if 'def_cat_uid' in postinfo.extinfo else None
            cat_enum1 = MCategory.get_qian2(ext_catid2[:2]) if ext_catid else []

        ######################################################



        catinfo = None
        p_catinfo = None

        post2catinfo = MPost2Catalog.get_first_category(postinfo.uid)

        catalog_infors = None
        if post2catinfo:
            catinfo = MCategory.get_by_uid(post2catinfo.tag_id)
            if catinfo:
                p_catinfo = MCategory.get_by_uid(catinfo.pid)
                catalog_infors = MPost2Catalog.query_pager_by_slug(catinfo.slug,
                                                                   current_page_num=1,
                                                                   order=True)

        kwd = {
            'pager': '',
            'url': self.request.uri,
            'daohangstr': '',
            'signature': postinfo.uid,
            'tdesc': '',
            'eval_0': MEvaluation.app_evaluation_count(postinfo.uid, 0),
            'eval_1': MEvaluation.app_evaluation_count(postinfo.uid, 1),
            'login': 1 if self.get_current_user() else 0,
            'has_image': 0,
            'parentlist': MCategory.get_parent_list(),
            'parentname': '',
            'catname': '',
            'router': router_post[postinfo.kind]
        }
        MPost.update_misc(postinfo.uid, count=True)
        if self.get_current_user():
            MUsage.add_or_update(self.userinfo.uid, postinfo.uid, postinfo.kind)

        tmpl = 'post_{0}/leaf_view.html'.format(self.kind)

        logger.info('The Info Template: {0}'.format(tmpl))

        self.render(tmpl,
                    kwd=dict(kwd, **self.ext_view_kwd(postinfo)),
                    postinfo=postinfo,
                    userinfo=self.userinfo,
                    catinfo=catinfo,
                    pcatinfo=p_catinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    ad_switch=random.randint(1, 18),
                    tag_info=MPost2Label.get_by_uid(postinfo.uid),
                    catalog_infos=catalog_infors,
                    cat_enum=cat_enum1)
