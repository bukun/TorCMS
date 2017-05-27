# -*- coding:utf-8 -*-

'''
Tornado Modules for infor.
'''

import tornado.web
from html2text import html2text

import torcms.model.usage_model
from config import router_post
from torcms.core.libs.deprecation import deprecated
from torcms.core.tools import logger
from torcms.model.category_model import MCategory
from torcms.model.label_model import MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
from torcms.model.relation_model import MRelation
from torcms.model.usage_model import MUsage


class InfoCategory(tornado.web.UIModule):
    '''
    List of category
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


class InforUserMost(tornado.web.UIModule):
    '''
    User most accessed posts.
    '''

    def render(self, user_name, kind, num, with_tag=False):
        all_cats = MUsage.query_most(user_name, kind, num).naive()
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
        }
        return self.render_string('modules/info/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)


class InfoUserRecent(tornado.web.UIModule):
    '''
    User used infors recently.
    '''

    @deprecated(details='should not used any more.')
    def render(self, user_name, kind, num, with_tag=False):
        all_cats = MUsage.query_recent(user_name, kind, num).naive()
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
        }
        return self.render_string('modules/info/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)


class InfoUserRecentByCategory(tornado.web.UIModule):
    '''
    User accessed posts recently by category.
    '''

    @deprecated(details='should not used any more.')
    def render(self, user_name, cat_id, num):
        all_cats = MUsage.query_recent_by_cat(user_name, cat_id, num).naive()

        return self.render_string('modules/info/list_user_equation_no_catalog.html',
                                  recs=all_cats)


class InfoMostUsedByCategory(tornado.web.UIModule):
    '''
    posts, most used of certain category.
    '''

    @deprecated(details='should not used any more.')
    def render(self, num, cat_str):
        all_cats = MPost.query_most_by_cat(num, cat_str)
        return self.render_string('modules/info/list_equation_by_cat.html',
                                  recs=all_cats)


class InfoLeastUseByCategory(tornado.web.UIModule):
    '''

    '''

    @deprecated(details='should not used any more.')
    def render(self, num, cat_str):
        all_cats = MPost.query_least_by_cat(num, cat_str)
        return self.render_string('modules/info/list_equation_by_cat.html', recs=all_cats)


class InfoMostUsed(tornado.web.UIModule):
    '''
    posts that most used.
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
        all_cats = MPost.query_most(kind=kind, num=num).naive()
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
        }
        return self.render_string('modules/info/list_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)

    def render_user(self, kind, num, with_tag=False, user_id=''):
        all_cats = MUsage.query_most(user_id, kind, num).naive()
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
        }
        return self.render_string('modules/info/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)


class InfoRecentUsed(tornado.web.UIModule):
    '''
    posts that recently used.
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
        if 'glyph' in kwargs:
            glyph = kwargs['glyph']
        else:
            glyph = None

        if userinfo:
            return self.render_user(kind, num, with_tag=with_tag, user_id=userinfo.uid, glyph=glyph)

        else:
            return self.render_it(kind, num, with_tag=with_tag, glyph=glyph)

    def render_it(self, kind, num, with_tag=False, glyph=''):
        '''
        render, no user logged in
        :param kind:
        :param num:
        :param with_tag:
        :return:
        '''
        all_cats = MPost.query_recent(num, kind=kind)
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
            'glyph': glyph
        }
        return self.render_string('modules/info/list_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)

    def render_user(self, kind, num, with_tag=False, user_id='', glyph=''):
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

        all_cats = MUsage.query_recent(user_id, kind, num).naive()
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
            'glyph': glyph
        }
        return self.render_string('modules/info/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)


class InfoRandom(tornado.web.UIModule):
    '''
    return some infors, randomly.
    '''

    def render(self, kind, num):
        all_cats = MPost.query_random(num=num, kind=kind)
        return self.render_string('modules/info/list_equation.html',
                                  recs=all_cats)


class InfoTags(tornado.web.UIModule):
    '''
    return tags of certain infor
    '''

    def render(self, *args):
        uid = args[0]
        out_str = ''
        iii = 1
        for tag_info in MPost2Catalog.query_by_entity_uid(uid).naive():
            tmp_str = '''<a data-inline="true" href="/tag/{0}"
             class="tag{1}">{2}</a>'''.format(tag_info.tag_slug, iii, tag_info.tag_name)
            out_str += tmp_str
            iii += 1
        return out_str


class LabelCount(tornado.web.UIModule):
    '''
    the count of certian tag.
    '''

    def render(self, *args):
        uid = args[0]
        return MPost2Label.query_count(uid)


class InfoMenu(tornado.web.UIModule):
    '''
    menu for infor.
    '''

    def render(self, kind, limit=10):
        all_cats = MCategory.query_field_count(limit, kind=kind)
        kwd = {
            'cats': all_cats,
        }
        return self.render_string('modules/info/app_menu.html', kwd=kwd)


# Todo: kind error.
class RelPost2app(tornado.web.UIModule):
    '''
    relation, post to app.
    '''

    def render(self, uid, num, ):
        kwd = {
            'app_f': 'post',
            'app_t': 'info',
            'uid': uid,
        }
        rel_recs = MRelation.get_app_relations(uid, num, kind='9').naive()

        rand_recs = MPost.query_random(num=num - rel_recs.count() + 2, kind='9')

        return self.render_string('modules/info/relation_post2app.html',
                                  relations=rel_recs,
                                  rand_recs=rand_recs,
                                  kwd=kwd, )


# Todo: kind error.
class RelApp2post(tornado.web.UIModule):
    '''
    relation, app to post.
    '''

    def render(self, uid, num, ):
        kwd = {
            'app_f': 'info',
            'app_t': 'post',
            'uid': uid,
        }
        rel_recs = MRelation.get_app_relations(uid, num, kind='1').naive()

        rand_recs = MPost.query_random(num=num - rel_recs.count() + 2, kind='1')

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
    Display userinfo.
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


class ParentName(tornado.web.UIModule):
    '''

    '''

    def render(self, info):
        return self.render_string('modules/info/parentname.html', info=info)


class CatName(tornado.web.UIModule):
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
