# -*- coding:utf-8 -*-

import random
import torcms.model.info_model
import torcms.model.usage_model
import tornado.web
from torcms.model.infor2label_model import MInfor2Label
from torcms.model.info_model import MInfor
from torcms.model.info_relation_model import *
from torcms.model.category_model import MCategory
import torcms.model.infor2catalog_model
from torcms.model.post_model import MPost
from html2text import html2text
from config import router_post


class app_catalog_of(tornado.web.UIModule):
    def render(self, uid_with_str, slug=False):
        self.mcat = MCategory()

        curinfo = self.mcat.get_by_uid(uid_with_str)

        sub_cats = self.mcat.query_sub_cat(uid_with_str)

        if slug:
            return self.render_string('modules/info/catalog_slug.html',
                                      pcatinfo=curinfo,
                                      sub_cats=sub_cats,
                                      recs=sub_cats, )
        else:
            return self.render_string('modules/info/catalog_of.html',
                                      pcatinfo=curinfo,
                                      sub_cats=sub_cats,
                                      recs=sub_cats,
                                      )


class app_user_most(tornado.web.UIModule):
    def render(self, user_name, kind, num, with_tag=False):
        self.mcat = torcms.model.usage_model.MUsage()
        all_cats = self.mcat.query_most(user_name, kind, num)
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
        }
        return self.render_string('modules/info/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)


class app_user_most_by_cat(tornado.web.UIModule):
    pass


class app_user_recent(tornado.web.UIModule):
    def render(self, user_name, kind, num, with_tag=False):
        self.mcat = torcms.model.usage_model.MUsage()
        all_cats = self.mcat.query_recent(user_name, kind, num)
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
        }
        return self.render_string('modules/info/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd,
                                  )


class app_user_recent_by_cat(tornado.web.UIModule):
    def render(self, user_name, cat_id, num):
        self.mcat = torcms.model.usage_model.MUsage()
        all_cats = self.mcat.query_recent_by_cat(user_name, cat_id, num)

        return self.render_string('modules/info/list_user_equation_no_catalog.html', recs=all_cats)


class app_most_used(tornado.web.UIModule):
    def render(self, kind, num, with_tag=False):
        self.mcat = torcms.model.info_model.MInfor()
        all_cats = self.mcat.query_most(kind, num)
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind],
        }
        return self.render_string('modules/info/list_equation.html', recs=all_cats,
                                  kwd=kwd,
                                  )


class app_most_used_by_cat(tornado.web.UIModule):
    def render(self, num, cat_str):
        self.mcat = torcms.model.info_model.MInfor()
        all_cats = self.mcat.query_most_by_cat(num, cat_str)
        return self.render_string('modules/info/list_equation_by_cat.html', recs=all_cats)


class app_least_use_by_cat(tornado.web.UIModule):
    def render(self, num, cat_str):
        self.mcat = torcms.model.info_model.MInfor()
        all_cats = self.mcat.query_least_by_cat(num, cat_str)
        return self.render_string('modules/info/list_equation_by_cat.html', recs=all_cats)


class app_recent_used(tornado.web.UIModule):
    def render(self, kind, num, with_tag=False):
        self.mcat = torcms.model.info_model.MInfor()
        all_cats = self.mcat.query_recent(num, kind=kind)
        kwd = {
            'with_tag': with_tag,
            'router': router_post[kind]
        }
        return self.render_string('modules/info/list_equation.html',
                                  recs=all_cats,
                                  kwd=kwd, )


class app_random_choose(tornado.web.UIModule):
    def render(self, kind, num):
        self.mcat = torcms.model.info_model.MInfor()
        all_cats = self.mcat.query_random(num=num, kind=kind)
        return self.render_string('modules/info/list_equation.html', recs=all_cats)


class app_tags(tornado.web.UIModule):
    def render(self, signature):
        print('-' * 10)
        print(signature)
        self.mapp2tag = torcms.model.infor2catalog_model.MInfor2Catalog()
        tag_infos = self.mapp2tag.query_by_entity_uid(signature)
        out_str = ''
        ii = 1
        for tag_info in tag_infos:
            tmp_str = '<a data-inline="true" href="/tag/{0}" class="tag{1}">{2}</a>'.format(tag_info.tag.slug, ii,
                                                                                            tag_info.tag.name)
            out_str += tmp_str
            ii += 1
        # print('info category', out_str)
        return out_str


class label_count(tornado.web.UIModule):
    def render(self, signature):
        self.mapp2tag = MInfor2Label()
        tag_infos = self.mapp2tag.query_count(signature)

        return tag_infos


class app_menu(tornado.web.UIModule):
    def render(self, kind, limit):
        self.mcat = MCategory()
        all_cats = self.mcat.query_field_count(limit, kind=kind)
        kwd = {
            'cats': all_cats,
        }
        return self.render_string('modules/info/app_menu.html', kwd=kwd)


class baidu_search(tornado.web.UIModule):
    def render(self, ):
        baidu_script = '''
        <script type="text/javascript">(function(){document.write(unescape('%3Cdiv id="bdcs"%3E%3C/div%3E'));var bdcs = document.createElement('script');bdcs.type = 'text/javascript';bdcs.async = true;bdcs.src = 'http://znsv.baidu.com/customer_search/api/js?sid=17856875184698336445' + '&plate_url=' + encodeURIComponent(window.location.href) + '&t=' + Math.ceil(new Date()/3600000);var s = document.getElementsByTagName('script')[0];s.parentNode.insertBefore(bdcs, s);})();</script>
        '''
        return self.render_string('modules/info/baidu_script.html',
                                  baidu_script=baidu_script)


class rel_post2app(tornado.web.UIModule):
    def render(self, uid, num, ):
        self.app = MInfor()
        self.relation = MRelPost2Infor()
        kwd = {
            'app_f': 'post',
            'app_t': 'info',
            'uid': uid,
        }
        rel_recs = self.relation.get_app_relations(uid, num, kind='2')

        rand_recs = self.app.query_random(num - rel_recs.count() + 2, kind='2')

        return self.render_string('modules/info/relation_post2app.html',
                                  relations=rel_recs,
                                  rand_recs=rand_recs,
                                  kwd=kwd, )


class rel_app2post(tornado.web.UIModule):
    def render(self, uid, num, ):
        self.mpost = MPost()
        self.relation = MRelInfor2Post()
        kwd = {
            'app_f': 'info',
            'app_t': 'post',
            'uid': uid,
        }
        rel_recs = self.relation.get_app_relations(uid, num, kind='1')

        rand_recs = self.mpost.query_random(num - rel_recs.count() + 2, kind='1')

        return self.render_string('modules/info/relation_app2post.html',
                                  relations=rel_recs,
                                  rand_recs=rand_recs,
                                  kwd=kwd, )


class ImgSlide(tornado.web.UIModule):
    def render(self, info):
        return self.render_string('modules/info/img_slide.html', post_info=info)


class UserInfo(tornado.web.UIModule):
    def render(self, uinfo, uop):
        return self.render_string('modules/info/user_info.html', userinfo=uinfo, userop=uop)


class VipInfo(tornado.web.UIModule):
    def render(self, uinfo, uvip):
        return self.render_string('modules/info/vip_info.html', userinfo=uinfo, uservip=uvip)


class BannerModule(tornado.web.UIModule):
    def __init__(self, parentid=''):
        self.parentid = parentid

    def render(self):
        self.mcat = MCategory()
        parentlist = self.mcat.get_parent_list()
        kwd = {
            'parentlist': parentlist,
            'parentid': self.parentid,
        }
        return self.render_string('modules/info/banner.html', kwd=kwd)


class BreadCrumb(tornado.web.UIModule):
    def render(self, info):
        return self.render_string('modules/info/bread_crumb.html', info=info)


class parentname(tornado.web.UIModule):
    def render(self, info):
        return self.render_string('modules/info/parentname.html', info=info)


class catname(tornado.web.UIModule):
    def render(self, info):
        return self.render_string('modules/info/catname.html', info=info)


class ContactInfo(tornado.web.UIModule):
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
    def render(self, sig=0):
        kwd = {
            'sig': sig,
        }
        return self.render_string('modules/info/breadcrumb_publish.html', kwd=kwd)


class InfoList:
    def renderit(self, info=''):
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
