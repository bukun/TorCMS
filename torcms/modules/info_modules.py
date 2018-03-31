# -*- coding:utf-8 -*-

'''
Tornado Modules for infor.
'''

import tornado.web
from html2text import html2text

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
        '''
        fun(uid_with_str)
        fun(uid_with_str, slug = val1, glyph = val2)
        '''

        uid_with_str = args[0]

        # if 'slug' in kwargs:
        #     slug = kwargs['slug']
        # else:
        #     slug = False
        slug = kwargs.get('slug', False)

        # if 'glyph' in kwargs:
        #     glyph = kwargs['glyph']
        # else:
        #     glyph = ''
        glyph = kwargs.get('glyph', '')

        kwd = {
            'glyph': glyph
        }
        curinfo = MCategory.get_by_uid(uid_with_str)

        sub_cats = MCategory.query_sub_cat(uid_with_str)

        if slug:
            tmpl = 'modules/info/catalog_slug.html'

        else:
            tmpl = 'modules/info/catalog_of.html'
        return self.render_string(tmpl,
                                  pcatinfo=curinfo,
                                  sub_cats=sub_cats,
                                  recs=sub_cats,
                                  kwd=kwd)


class InforUserMost(tornado.web.UIModule):
    '''
    User most accessed posts.
    '''

    def render(self, *args, **kwargs):
        '''
        fun(user_name, kind)
        fun(user_name, kind, num)
        fun(user_name, kind, num, with_tag = val1, glyph = val2)
        fun(user_name = vala, kind = valb, num = valc, with_tag = val1, glyph = val2)
        '''

        # kind = kwargs.get('kind', args[0] if len(args) > 0 else '1')

        # user_name = args[0]
        # kind = args[1]
        # num = args[2]
        # with_tag = kwargs['with_tag'] if 'with_tag' in kwargs else False
        # glyph = kwargs['glyph'] if 'glyph' in kwargs else ''

        user_name = kwargs.get('user_name', args[0])
        kind = kwargs.get('kind', args[1])
        num = kwargs.get('num', args[2] if len(args) > 2 else 6)
        with_tag = kwargs.get('with_tag', False)
        glyph = kwargs.get('glyph', '')

        all_cats = MUsage.query_most(user_name, kind, num).objects()
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
            'glyph': glyph
        }
        return self.render_string('modules/info/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)


class InfoUserRecent(tornado.web.UIModule):
    '''
    User used infors recently.
    '''

    @deprecated(details='should not used any more.')
    def render(self, *args, **kwargs):
        '''
        fun(user_name, kind)
        fun(user_name, kind, num)
        fun(user_name, kind, num, with_tag = val1, glyph = val2)
        fun(user_name = vala, kind = valb, num = valc, with_tag = val1, glyph = val2)
        '''

        # user_name = args[0]
        # kind = args[1]
        # num = args[2]
        # with_tag = kwargs['with_tag'] if 'with_tag' in kwargs else False
        # glyph = kwargs['glyph'] if 'glyph' in kwargs else ''

        user_name = kwargs.get('user_name', args[0])
        kind = kwargs.get('kind', args[1])
        num = kwargs.get('num', args[2] if len(args) > 2 else 6)
        with_tag = kwargs.get('with_tag', False)
        glyph = kwargs.get('glyph', '')

        all_cats = MUsage.query_recent(user_name, kind, num).objects()
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
            'glyph': glyph
        }
        return self.render_string('modules/info/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)


class InfoUserRecentByCategory(tornado.web.UIModule):
    '''
    User accessed posts recently by category.
    '''

    @deprecated(details='should not used any more.')
    def render(self, *args, **kwargs):
        '''
        fun(user_name, catid)
        fun(user_name, catid, num)
        fun(user_name, catid, num, glyph = val1)
        '''

        # user_name = args[0]
        # cat_id = args[1]
        # num = args[2]
        # glyph = kwargs['glyph'] if 'glyph' in kwargs else ''

        user_name = kwargs.get('user_name', args[0])
        cat_id = kwargs.get('cat_id', args[1])
        num = kwargs.get('num', args[2] if len(args) > 2 else 6)
        glyph = kwargs.get('glyph', '')

        all_cats = MUsage.query_recent_by_cat(user_name, cat_id, num).objects()
        kwd = {

            'glyph': glyph
        }
        return self.render_string('modules/info/list_user_equation_no_catalog.html',
                                  recs=all_cats,
                                  kwd=kwd)


class InfoMostUsedByCategory(tornado.web.UIModule):
    '''
    posts, most used of certain category.
    '''

    @deprecated(details='should not used any more.')
    def render(self, *args, **kwargs):
        '''
        fun(num, cat_str)
        fun(num, cat_str, glyph = val1)

        下面查询语句 query_most_by_cat 中有kind这一参数，所以又加了一种情况：
        fun(num, cat_str, glyph = val1, kind = val2)
        '''

        # num = args[0]
        # cat_str = args[1]
        # glyph = kwargs['glyph'] if 'glyph' in kwargs else ''

        num = kwargs.get('num', args[0])
        cat_str = kwargs.get('cat_str', args[1])
        glyph = kwargs.get('glyph', '')
        kind = kwargs.get('kind', '')

        # all_cats = MPost.query_most_by_cat(num, cat_str)
        all_cats = MPost.query_most_by_cat(num, cat_str, kind)
        kwd = {
            'glyph': glyph
        }
        return self.render_string('modules/info/list_equation_by_cat.html',
                                  recs=all_cats,
                                  kwd=kwd)


class InfoLeastUseByCategory(tornado.web.UIModule):
    '''
    Deprecated
    '''

    @deprecated(details='should not used any more.')
    def render(self, *args, **kwargs):
        '''
        fun(num, cat_str)
        fun(num, cat_str, glyph = val1)
        '''

        # num = args[0]
        # cat_str = args[1]
        # glyph = kwargs['glyph'] if 'glyph' in kwargs else ''

        num = kwargs.get('num', args[0])
        cat_str = kwargs.get('cat_str', args[1])
        glyph = kwargs.get('glyph', '')

        all_cats = MPost.query_least_by_cat(num, cat_str)
        kwd = {

            'glyph': glyph
        }
        return self.render_string('modules/info/list_equation_by_cat.html', recs=all_cats, kwd=kwd)


class InfoMostUsed(tornado.web.UIModule):
    '''
    posts that most used.
    '''

    def render(self, *args, **kwargs):

        kind = kwargs.get('kind', args[0] if args else '1')
        num = kwargs.get('num', args[1] if len(args) > 1 else 6)

        with_tag = kwargs.get('with_tag', False)
        userinfo = kwargs.get('userinfo', None)
        glyph = kwargs.get('glyph', '')

        if userinfo:
            html_str = self.render_user(kind,
                                        num,
                                        with_tag=with_tag,
                                        user_id=userinfo.uid,
                                        glyph=glyph)
        else:
            html_str = self.render_it(kind, num, with_tag=with_tag, glyph=glyph)
        return html_str

    def render_it(self, *args, **kwargs):
        '''
        Render without userinfo.
        fun(kind, num)
        fun(kind, num, with_tag = val1)
        fun(kind, num, with_tag = val1, glyph = val2)
        '''

        # kind = args[0]
        # num = args[1]
        #
        # with_tag = kwargs['with_tag'] if 'with_tag' in kwargs else False
        #
        # glyph = kwargs['glyph'] if 'glyph' in kwargs else  ''

        kind = kwargs.get('kind', args[0])
        num = kwargs.get('num', args[1] if len(args) > 1 else 6)
        with_tag = kwargs.get('with_tag', False)
        glyph = kwargs.get('glyph', '')

        all_cats = MPost.query_most(kind=kind, num=num).objects()
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
            'glyph': glyph
        }
        return self.render_string('modules/info/list_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)

    def render_user(self, *args, **kwargs):
        '''
        Render user.
        fun(kind, num)
        fun(kind, num, with_tag = val1)
        fun(kind, num, with_tag = val1, user_id = val2)
        fun(kind, num, with_tag = val1, user_id = val2, glyph = val3)
        '''

        # kind = args[0]
        # num = args[1]
        #
        # with_tag = kwargs['with_tag'] if 'with_tag' in kwargs else False
        #
        # user_id = kwargs['user_id'] if 'user_id' in kwargs else ''
        #
        # glyph = kwargs['glyph'] if 'glyph' in kwargs else  ''

        kind = kwargs.get('kind', args[0])
        num = kwargs.get('num', args[1] if len(args) > 1 else 6)
        with_tag = kwargs.get('with_tag', False)
        user_id = kwargs.get('user_id', '')
        glyph = kwargs.get('glyph', '')

        all_cats = MUsage.query_most(user_id, kind, num).objects()
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
            'glyph': glyph
        }
        return self.render_string('modules/info/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)


class InfoRecentUsed(tornado.web.UIModule):
    '''
    posts that recently used.
    '''

    def render(self, *args, **kwargs):

        kind = kwargs.get('kind', args[0] if args else '1')
        num = kwargs.get('num', args[1] if len(args) > 1 else 6)

        with_tag = kwargs.get('with_tag', False)
        userinfo = kwargs.get('userinfo', None)
        glyph = kwargs.get('glyph', '')

        if userinfo:
            html_str = self.render_user(
                kind,
                num,
                with_tag=with_tag,
                user_id=userinfo.uid,
                glyph=glyph
            )
        else:
            html_str = self.render_it(kind, num, with_tag=with_tag, glyph=glyph)
        return html_str

    def render_it(self, kind, num, with_tag=False, glyph=''):
        '''
        render, no user logged in
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

    def render_user(self, *args, **kwargs):
        '''
        render, with userinfo
        fun(kind, num)
        fun(kind, num, with_tag = val1)
        fun(kind, num, with_tag = val1, user_id = val2)
        fun(kind, num, with_tag = val1, user_id = val2, glyph = val3)
        '''

        # kind = args[0]
        # num = args[1]
        #
        # with_tag = kwargs['with_tag'] if 'with_tag' in kwargs else False
        #
        # user_id = kwargs['user_id'] if 'user_id' in kwargs else ''
        #
        # glyph = kwargs['glyph'] if 'glyph' in kwargs else  ''

        kind = kwargs.get('kind', args[0])
        num = kwargs.get('num', args[1] if len(args) > 1 else 6)
        with_tag = kwargs.get('with_tag', False)
        user_id = kwargs.get('user_id', '')
        glyph = kwargs.get('glyph', '')

        logger.info(
            'Infor user recent, username: {user_name}, kind: {kind}, num: {num}'.format(
                user_name=user_id, kind=kind, num=num
            )
        )

        all_cats = MUsage.query_recent(user_id, kind, num).objects()
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
    fun(kind, num)
    fun(kind, num, glyph = val1)
    '''

    def render(self, *args, **kwargs):
        # kind = args[0]
        # num = args[1]

        kind = kwargs.get('kind', args[0])
        num = kwargs.get('num', args[1] if len(args) > 1 else 6)
        glyph = kwargs.get('glyph', '')

        all_cats = MPost.query_random(num=num, kind=kind)
        kwd = {

            'glyph': glyph
        }
        return self.render_string('modules/info/list_equation.html',
                                  recs=all_cats, kwd=kwd)


class InfoTags(tornado.web.UIModule):
    '''
    return tags of certain infor
    fun(uid)
    '''

    def render(self, *args, **kwargs):
        # uid = args[0]

        uid = kwargs.get('uid', args[0])

        out_str = ''
        iii = 1
        for tag_info in MPost2Catalog.query_by_entity_uid(uid).objects():
            tmp_str = '''<a data-inline="true" href="/tag/{0}"
             class="tag{1}">{2}</a>'''.format(tag_info.tag_slug, iii, tag_info.tag_name)
            out_str += tmp_str
            iii += 1
        return out_str


class LabelCount(tornado.web.UIModule):
    '''
    the count of certian tag.
    fun(uid)
    '''

    def render(self, *args, **kwargs):
        # uid = args[0]

        uid = kwargs.get('uid', args[0])
        return MPost2Label.query_count(uid)


class InfoMenu(tornado.web.UIModule):
    '''
    menu for infor.
    fun(kind)
    fun(kind, limit)
    '''

    def render(self, *args, **kwargs):
        # kind = args[0]

        kind = kwargs.get('kind', args[0])
        limit = kwargs.get('limit', 10)
        all_cats = MCategory.query_field_count(limit, kind=kind)
        kwd = {
            'cats': all_cats,
        }
        return self.render_string('modules/info/app_menu.html', kwd=kwd)


# Todo:  To test the class.
class RelPost2app(tornado.web.UIModule):
    '''
    relation, post to app.
    fun(uid, num)
    fun(uid, num, kind = val1)
    fun(uid, num, kind = val1, num = val2)
    '''

    def render(self, *args, **kwargs):
        # uid = args[0]
        # num = args[1] if len(args) > 1 else 6
        # kind = kwargs['kind'] if 'kind' in kwargs else '1'
        # num = kwargs['num'] if 'num' in kwargs else num

        uid = kwargs.get('uid', args[0])
        num = kwargs.get('num', args[1] if len(args) > 1 else 6)
        kind = kwargs.get('kind', '1')

        kwd = {
            'app_f': 'post',
            'app_t': 'info',
            'uid': uid,
        }
        rel_recs = MRelation.get_app_relations(uid, num, kind=kind).objects()

        rand_recs = MPost.query_random(num=num - rel_recs.count() + 2, kind=kind)

        return self.render_string('modules/info/relation_post2app.html',
                                  relations=rel_recs,
                                  rand_recs=rand_recs,
                                  kwd=kwd, )


# Todo: To test the class.
class RelApp2post(tornado.web.UIModule):
    '''
    relation, app to post.
    fun(uid, num)
    fun(uid, num, kind = val1)
    fun(uid, num, kind = val1, num = val2)
    '''

    def render(self, *args, **kwargs):
        # uid = args[0]
        # num = args[1] if len(args) > 1 else 6
        # num = kwargs['num'] if 'num' in kwargs else num
        # kind = kwargs['kind'] if 'kind' in kwargs else '1'

        uid = kwargs.get('uid', args[0])
        num = kwargs.get('num', args[1] if len(args) > 1 else 6)
        kind = kwargs.get('kind', '1')

        kwd = {
            'app_f': 'info',
            'app_t': 'post',
            'uid': uid,
        }
        rel_recs = MRelation.get_app_relations(uid, num, kind=kind).objects()

        rand_recs = MPost.query_random(num=num - rel_recs.count() + 2, kind=kind)

        return self.render_string('modules/info/relation_app2post.html',
                                  relations=rel_recs,
                                  rand_recs=rand_recs,
                                  kwd=kwd)


class ImgSlide(tornado.web.UIModule):
    '''
    Module for Image slide.
    fun(info)
    '''

    def render(self, *args, **kwargs):
        # info = args[0]

        info = kwargs.get('info', args[0])
        return self.render_string('modules/info/img_slide.html', post_info=info)


class UserInfo(tornado.web.UIModule):
    '''
    Display userinfo.
    fun(uinfo, uop)
    '''

    def render(self, *args, **kwargs):
        # uinfo = args[0]
        # uop = args[1]

        uinfo = kwargs.get('uinfo', args[0])
        uop = kwargs.get('uop', args[1])
        return self.render_string('modules/info/user_info.html', userinfo=uinfo, userop=uop)


class VipInfo(tornado.web.UIModule):
    '''
    VipInfo
    fun(uinfo, uvip)
    '''

    def render(self, *args, **kwargs):
        # uinfo = args[0]
        # uvip = args[1]

        uinfo = kwargs.get('uinfo', args[0])
        uvip = kwargs.get('uvip', args[1])
        return self.render_string('modules/info/vip_info.html', userinfo=uinfo, uservip=uvip)


class BannerModule(tornado.web.UIModule):
    '''
    BannerModule
    fun(parentid = val)
    '''

    def render(self, *args, **kwargs):
        # parentid = kwargs['parentid'] if 'parentid' in kwargs else ''

        parentid = kwargs.get('parentid', '')
        parentlist = MCategory.get_parent_list()
        kwd = {
            'parentlist': parentlist,
            'parentid': parentid,
        }
        return self.render_string('modules/info/banner.html', kwd=kwd)


class BreadCrumb(tornado.web.UIModule):
    '''
    BreadCrumb
    fun(info)
    '''

    def render(self, *args, **kwargs):
        # info = args[0]

        info = kwargs.get('info', args[0])
        return self.render_string('modules/info/bread_crumb.html', info=info)


class ParentName(tornado.web.UIModule):
    '''
    ParentName
    fun(info)
    '''

    def render(self, *args, **kwargs):
        # info = args[0]

        info = kwargs.get('info', args[0])
        return self.render_string('modules/info/parentname.html', info=info)


class CatName(tornado.web.UIModule):
    '''
    CatName
    fun(info)
    '''

    def render(self, *args, **kwargs):
        # info = args[0]

        info = kwargs.get('info', args[0])
        return self.render_string('modules/info/catname.html', info=info)


class ContactInfo(tornado.web.UIModule):
    '''
    ContactInfo
    fun(info)
    '''

    def render(self, *args, **kwargs):
        # info = args[0]

        info = kwargs.get('info', args[0])
        kwd = {
            'maskip': '',  # maskip,
        }
        return self.render_string('modules/info/contact_info.html', post_info=info, kwd=kwd)


class BreadcrumbPublish(tornado.web.UIModule):
    '''
    BreadCrumb
    fun(sig = val1)
    '''

    def render(self, *args, **kwargs):
        # sig = kwargs['sig'] if 'sig' in kwargs else  0

        sig = kwargs.get('sig', 0)
        kwd = {
            'sig': sig,
        }
        return self.render_string('modules/info/breadcrumb_publish.html', kwd=kwd)


class InfoList(tornado.web.UIModule):
    '''
    InfoList.
    fun(info)
    '''

    def render(self, *args, **kwargs):

        # info = args[0]

        info = kwargs.get('info', args[0])
        zhiding_str = ''
        tuiguang_str = ''
        imgname = 'fixed/zhanwei.png'
        if info.extinfo['mymps_img']:
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
