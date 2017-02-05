# -*- coding:utf-8 -*-

'''
Tornado Modules for infor.
'''

import torcms.model.info_model
import torcms.model.usage_model
import tornado.web
from torcms.model.label_model import MPost2Label
from torcms.model.info_model import MInfor
from torcms.model.relation_model import MRelation

from torcms.model.post2catalog_model import MPost2Catalog

from torcms.model.category_model import MCategory
from torcms.model.post_model import MPost
from html2text import html2text
from config import router_post
from torcms.core.tools import logger
from torcms.core.libs.deprecated import deprecated


class InfoCategory(tornado.web.UIModule):
    '''

    '''

    def render(self, *args, **kwargs):
        uid_with_str = args[0]
        if 'slug' in kwargs:
            slug = kwargs['slug']
        else:
            slug = False

        curinfo = MCategory.get_by_uid(uid_with_str)

        sub_cats = MCategory.query_sub_cat(uid_with_str)

        if slug:
            return self.render_string('modules/info/catalog_slug.html',
                                      pcatinfo=curinfo,
                                      sub_cats=sub_cats,
                                      recs=sub_cats)
        else:
            return self.render_string('modules/info/catalog_of.html',
                                      pcatinfo=curinfo,
                                      sub_cats=sub_cats,
                                      recs=sub_cats)


@deprecated
class InforUserMost(tornado.web.UIModule):
    '''

    '''

    def render(self, user_name, kind, num, with_tag=False):
        all_cats = torcms.model.usage_model.MUsage.query_most(user_name, kind, num)
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
        }
        return self.render_string('modules/info/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)


class app_user_most_by_cat(tornado.web.UIModule):
    '''

    '''
    pass


@deprecated
class InfoUserRecent(tornado.web.UIModule):
    '''

    '''

    def render(self, user_name, kind, num, with_tag=False):
        logger.info('Infor user recent, username: {user_name}, kind: {kind}, num: {num}'.format(
            user_name=user_name, kind=kind, num=num
        ))

        all_cats = torcms.model.usage_model.MUsage.query_recent(user_name, kind, num)
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
        }
        return self.render_string('modules/info/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)


class app_user_recent_by_cat(tornado.web.UIModule):
    '''

    '''

    def render(self, user_name, cat_id, num):
        all_cats = torcms.model.usage_model.MUsage.query_recent_by_cat(user_name, cat_id, num)

        return self.render_string('modules/info/list_user_equation_no_catalog.html',
                                  recs=all_cats)


class InfoMostUsed(tornado.web.UIModule):
    '''

    '''

    def render(self, kind, num, **kwargs):

        if 'with_tag' in kwargs:
            with_tag = kwargs['with_tag']
        else:
            with_tag = False

        if 'userinfo' in kwargs:
            userinfo = kwargs['userinfo']
        else:
            userinfo = None

        if userinfo:
            return self.render_user(kind, num, with_tag=with_tag, user_id=userinfo.uid)
        else:
            return self.render_it(kind, num, with_tag=with_tag)

    def render_it(self, kind, num, with_tag=False):
        all_cats = torcms.model.info_model.MInfor.query_most(kind, num)
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
        }
        return self.render_string('modules/info/list_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)

    def render_user(self, kind, num, with_tag=False, user_id=''):
        all_cats = torcms.model.usage_model.MUsage.query_most(user_id, kind, num)
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
        }
        return self.render_string('modules/info/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)


class app_most_used_by_cat(tornado.web.UIModule):
    '''

    '''

    def render(self, num, cat_str):
        all_cats = torcms.model.info_model.MInfor.query_most_by_cat(num, cat_str)
        return self.render_string('modules/info/list_equation_by_cat.html',
                                  recs=all_cats)


class app_least_use_by_cat(tornado.web.UIModule):
    '''

    '''

    def render(self, num, cat_str):
        all_cats = torcms.model.info_model.MInfor.query_least_by_cat(num, cat_str)
        return self.render_string('modules/info/list_equation_by_cat.html', recs=all_cats)


class InfoRecentUsed(tornado.web.UIModule):
    '''

    '''
    def render(self, kind, num, **kwargs):

        if 'with_tag' in kwargs:
            with_tag = kwargs['with_tag']
        else:
            with_tag = False

        if 'userinfo' in kwargs:
            userinfo = kwargs['userinfo']
        else:
            userinfo = None

        if userinfo:
            return self.render_user(kind, num, with_tag=with_tag, user_id=userinfo.uid)

        else:
            return self.render_it(kind, num, with_tag=with_tag)

    def render_it(self, kind, num, with_tag=False):
        '''
        render, no user logged in
        :param kind:
        :param num:
        :param with_tag:
        :return:
        '''
        all_cats = torcms.model.info_model.MInfor.query_recent(num, kind=kind)
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind]
        }
        return self.render_string('modules/info/list_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)

    def render_user(self, kind, num, with_tag=False, user_id=''):
        '''
        render, with userinfo
        :param kind:
        :param num:
        :param with_tag:
        :param user_id:
        :return:
        '''
        logger.info('Infor user recent, username: {user_name}, kind: {kind}, num: {num}'.format(
            user_name=user_id, kind=kind, num=num
        ))

        all_cats = torcms.model.usage_model.MUsage.query_recent(user_id, kind, num)
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
        }
        return self.render_string('modules/info/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)


class app_random_choose(tornado.web.UIModule):
    '''

    '''
    def render(self, kind, num):
        all_cats = torcms.model.info_model.MInfor.query_random(num=num, kind=kind)
        return self.render_string('modules/info/list_equation.html',
                                  recs=all_cats)


class app_tags(tornado.web.UIModule):
    '''

    '''
    def render(self, signature):
        out_str = ''
        ii = 1
        for tag_info in MPost2Catalog.query_by_entity_uid(signature):
            tmp_str = '''<a data-inline="true" href="/tag/{0}"
             class="tag{1}">{2}</a>'''.format(tag_info.tag.slug, ii, tag_info.tag.name)
            out_str += tmp_str
            ii += 1
        return out_str


class label_count(tornado.web.UIModule):
    '''

    '''
    def render(self, signature):
        return MPost2Label.query_count(signature)


class app_menu(tornado.web.UIModule):
    '''

    '''
    def render(self, kind, limit=10):
        all_cats = MCategory.query_field_count(limit, kind=kind)
        kwd = {
            'cats': all_cats,
        }
        return self.render_string('modules/info/app_menu.html', kwd=kwd)


class baidu_search(tornado.web.UIModule):
    '''

    '''
    def render(self, ):
        baidu_script = ''
        return self.render_string('modules/info/baidu_script.html',
                                  baidu_script=baidu_script)


class rel_post2app(tornado.web.UIModule):
    '''

    '''
    def render(self, uid, num, ):
        kwd = {
            'app_f': 'post',
            'app_t': 'info',
            'uid': uid,
        }
        rel_recs = MRelation.get_app_relations(uid, num, kind='2')

        rand_recs = MInfor.query_random(num - rel_recs.count() + 2, kind='2')

        return self.render_string('modules/info/relation_post2app.html',
                                  relations=rel_recs,
                                  rand_recs=rand_recs,
                                  kwd=kwd, )


class rel_app2post(tornado.web.UIModule):
    '''

    '''
    def render(self, uid, num, ):
        kwd = {
            'app_f': 'info',
            'app_t': 'post',
            'uid': uid,
        }
        rel_recs = MRelation.get_app_relations(uid, num, kind='1')

        rand_recs = MPost.query_random(num - rel_recs.count() + 2, kind='1')

        return self.render_string('modules/info/relation_app2post.html',
                                  relations=rel_recs,
                                  rand_recs=rand_recs,
                                  kwd=kwd)


class ImgSlide(tornado.web.UIModule):
    '''

    '''
    def render(self, info):
        return self.render_string('modules/info/img_slide.html', post_info=info)


class UserInfo(tornado.web.UIModule):
    '''

    '''
    def render(self, uinfo, uop):
        return self.render_string('modules/info/user_info.html', userinfo=uinfo, userop=uop)


class VipInfo(tornado.web.UIModule):
    '''

    '''
    def render(self, uinfo, uvip):
        return self.render_string('modules/info/vip_info.html', userinfo=uinfo, uservip=uvip)


class BannerModule(tornado.web.UIModule):
    '''

    '''
    def render(self, parentid=''):
        parentlist = MCategory.get_parent_list()
        kwd = {
            'parentlist': parentlist,
            'parentid': parentid,
        }
        return self.render_string('modules/info/banner.html', kwd=kwd)


class BreadCrumb(tornado.web.UIModule):
    '''

    '''
    def render(self, info):
        return self.render_string('modules/info/bread_crumb.html', info=info)


class parentname(tornado.web.UIModule):
    '''

    '''
    def render(self, info):
        return self.render_string('modules/info/parentname.html', info=info)


class catname(tornado.web.UIModule):
    '''

    '''
    def render(self, info):
        return self.render_string('modules/info/catname.html', info=info)


class ContactInfo(tornado.web.UIModule):
    '''

    '''
    def render(self, info):
        # ip_addr = info.extinfo['userip'][0]
        # ip_arr = ip_addr.split('.')
        # if len(ip_arr) > 3:
        #     ip_arr[3] = '*'
        # maskip = '.'.join(ip_arr)
        kwd = {
            'maskip': '',  # maskip,
        }
        return self.render_string('modules/info/contact_info.html', post_info=info, kwd=kwd)


class BreadcrumbPublish(tornado.web.UIModule):
    '''

    '''
    def render(self, sig=0):
        kwd = {
            'sig': sig,
        }
        return self.render_string('modules/info/breadcrumb_publish.html', kwd=kwd)


class InfoList(tornado.web.UIModule):
    '''

    '''
    def renderit(self, info):
        zhiding_str = ''
        tuiguang_str = ''
        imgname = 'fixed/zhanwei.png'
        if len(info.extinfo['mymps_img']) > 0:
            imgname = info.extinfo['mymps_img'][0]
        if info.extinfo['def_zhiding'] == 1:
            zhiding_str = '<span class="red">（已置顶）</span>'
        if info.extinfo['def_tuiguang'] == 1:
            tuiguang_str = '<span class="red">（已推广）</span>'

        list_type = info.extinfo['catid']

        kwd = {
            'imgname': imgname,
            'zhiding': zhiding_str,
            'tuiguan': tuiguang_str,
        }

        return self.render_string('infor/infolist/infolist_{0}.html'.format(list_type),
                                  kwd=kwd,
                                  html2text=html2text,
                                  post_info=info)
