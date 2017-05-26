# -*- coding:utf-8 -*-

import json
import tornado.escape
import tornado.web
import config
from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.category_model import MCategory


class MaintainCategoryHandler(BaseHandler):
    def initialize(self):
        super(MaintainCategoryHandler, self).initialize()
        self.tmpl_router = 'maintain_category'

    def get(self, *args):
        url_str = args[0]

        url_arr = self.parse_url(url_str)

        if url_str == 'add':
            self.to_add()
        elif url_str == 'list':
            self.list_catalog()
        elif url_arr[0] == 'modify':
            self.to_modify(url_arr[1])
        elif url_arr[0] == 'delete':
            self.delete_by_uid(url_arr[1])

        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo, )

    def post(self, *args):
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        if url_arr[0] == 'modify':
            self.update(url_arr[1])
        elif url_str == 'add':
            self.p_add_catalog()
        elif url_arr[0] == 'add':

            self.p_add_catalog()
        else:
            self.redirect('misc/html/404.html')

    def list_catalog(self):
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': '最近文档',
        }
        self.render('admin/{0}/category_list.html'.format(self.tmpl_router),
                    kwd=kwd,
                    view=MCategory.query_all(by_order=True),
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    cfg=config.CMS_CFG)

    @tornado.web.authenticated
    def to_add(self):
        if self.check_post_role()['ADD']:
            pass
        else:
            return False
        kwd = {
            'pager': '',
            'uid': '',
        }
        self.render('admin/{0}/category_add.html'.format(self.tmpl_router),
                    topmenu='',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    cfg=config.CMS_CFG)

    def __could_edit(self, uid):
        raw_data = MCategory.get_by_uid(uid)
        if not raw_data:
            return False
        if self.check_post_role()['EDIT'] or raw_data.id_user == self.userinfo.user_name:
            return True
        else:
            return False

    @tornado.web.authenticated
    def update(self, uid):
        if self.__could_edit(uid):
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        post_data['user_name'] = self.get_current_user()

        if self.tmpl_router == "maintain_category":
            MCategory.update(uid, post_data)
            self.redirect('/maintain/category/list')
        else:
            if MCategory.update(uid, post_data):

                output = {
                    'addinfo ': 1,
                }
            else:
                output = {
                    'addinfo ': 0,
                }
            return json.dump(output, self)

    @tornado.web.authenticated
    def to_modify(self, id_rec):
        if self.__could_edit(id_rec):
            pass
        else:
            return False
        a = MCategory.get_by_uid(id_rec)
        kwd = {
            'pager': '',

        }
        self.render('admin/{0}/category_edit.html'.format(self.tmpl_router),
                    kwd=kwd,
                    unescape=tornado.escape.xhtml_unescape,
                    dbrec=a,
                    userinfo=self.userinfo,
                    cfg=config.CMS_CFG, )

    @tornado.web.authenticated
    def add_post(self):
        if self.check_post_role()['ADD']:
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        post_data['user_name'] = self.get_current_user()
        id_post = post_data['uid'][0]
        cur_post_rec = MCategory.get_by_uid(id_post)
        if cur_post_rec is None:
            uid = MCategory.add_or_update(id_post, post_data)

        self.redirect('/maintain/category/list')

    @tornado.web.authenticated
    def p_add_catalog(self):

        if self.check_post_role()['ADD']:
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        post_data['user_name'] = self.get_current_user()

        cur_uid = tools.get_uudd(2)
        while MCategory.get_by_uid(cur_uid):
            cur_uid = tools.get_uudd(2)

        if MCategory.add_or_update(post_data['uid'][0], post_data):

            output = {
                'addinfo ': 1,
            }
        else:
            output = {
                'addinfo ': 0,
            }
        return json.dump(output, self)

    @tornado.web.authenticated
    def add_catalog(self):
        if self.check_post_role()['ADD']:
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        post_data['user_name'] = self.get_current_user()

        cur_uid = tools.get_uudd(2)
        while MCategory.get_by_uid(cur_uid):
            cur_uid = tools.get_uudd(2)

        uid = MCategory.add_or_update(cur_uid, post_data)

        self.redirect('/maintain/category/list')

    @tornado.web.authenticated
    def delete_by_uid(self, del_id):
        if self.check_post_role()['DELETE']:
            pass
        else:
            return False
        if self.tmpl_router == "maintain_category":
            is_deleted = MCategory.delete(del_id)

            if is_deleted:
                self.redirect('/maintain/category/list')
            else:
                return False
        else:
            if MCategory.delete(del_id):
                output = {
                    'del_category': 1
                }
            else:
                output = {
                    'del_category': 0,
                }

            return json.dump(output, self)


class MaintainCategoryAjaxHandler(MaintainCategoryHandler):
    def initialize(self):
        super(MaintainCategoryAjaxHandler, self).initialize()
        self.tmpl_router = 'category_ajax'
