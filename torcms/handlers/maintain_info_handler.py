# -*- coding:utf-8 -*-

import tornado.escape
import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.model.category_model import MCategory

from torcms.core import tools


class MaintainPycateCategoryHandler(BaseHandler):
    def initialize(self):
        super(MaintainPycateCategoryHandler, self).initialize()
        self.mclass = MCategory()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_str == 'add':
            self.to_add_class()
        elif url_str == 'list':
            self.recent()
        elif url_str == 'refresh':
            self.refresh()
        elif url_arr[0] == 'modify':
            self.to_modify(url_arr[1])
        elif url_arr[0] == 'delete':
            self.delete(url_arr[1])

        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('html/404.html', kwd=kwd)

    def post(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1 and url_str.endswith('.html'):
            self.add_post()

        if url_arr[0] == 'modify':
            self.update(url_arr[1])
        elif url_str == 'add':
            self.user_add_class()
        else:
            self.redirect('html/404.html')

    def recent(self):
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': '最近文档',
        }
        self.render('doc/maintain/pycatecategory/category_list.html',
                    kwd=kwd,
                    view=self.mclass.query_recent(),
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    )

    def refresh(self):

        kwd = {
            'pager': '',
            'title': '最近文档',
        }
        self.render('doc/maintain/pycatecategory/category_list.html',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    view=self.mclass.query_dated(10),
                    format_date=tools.format_date,
                    unescape=tornado.escape.xhtml_unescape, )

    def get_random(self):
        return self.mclass.query_random()

    def wiki(self, uid):
        dbdate = self.mclass.get_by_id(uid)
        if dbdate:

            self.viewit(uid)
        else:

            self.to_add(uid)

    def to_add_class(self, ):
        kwd = {
            'pager': '',
            'uid': '',
        }
        self.render('doc/maintain/pycatecategory/category_add.html',
                    topmenu='',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    )

    @tornado.web.authenticated
    def to_add(self, uid):
        if self.is_admin():
            pass
        else:
            return False
        kwd = {
            'uid': uid,
            'pager': '',
        }
        self.render('doc/maintain/pycatecategory/list.html',
                    kwd=kwd,
                    )

    @tornado.web.authenticated
    def update(self, uid):
        if self.is_admin():
            pass
        else:
            return False
        raw_data = self.mclass.get_by_id(uid)

        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        post_data['user_name'] = self.get_current_user()

        self.mclass.update(uid, post_data)

        self.redirect('/maintain/pycatecategory/list'.format(uid))

    @tornado.web.authenticated
    def to_modify(self, id_rec):
        a = self.mclass.get_by_id(id_rec)
        # 用户具有管理权限，或文章是用户自己发布的。
        if self.is_admin():
            pass
        else:
            return False

        kwd = {
            'pager': '',

        }
        self.render('doc/maintain/pycatecategory/category_edit.html',
                    kwd=kwd,
                    unescape=tornado.escape.xhtml_unescape,
                    dbrec=a,
                    userinfo=self.userinfo,
                    )

    @tornado.web.authenticated
    def viewit(self, post_id):

        rec = self.mclass.get_by_uid(post_id)

        if not rec:
            kwd = {
                'info': '您要找的分类不存在。',
            }
            self.render('html/404.html', kwd=kwd)
            return False

        kwd = {
            'pager': '',
            'editable': self.editable(),

        }

        self.render('doc/maintain/pycatecategory/category_view.html',
                    view=rec,
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    userinfo=self.userinfo,

                    )

    @tornado.web.authenticated
    def user_add_class(self):
        if self.is_admin():
            pass
        else:
            return False
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        post_data['user_name'] = self.get_current_user()

        self.mclass.insert_data(post_data)

        self.redirect('/maintain/pycatecategory/list'.format())

    @tornado.web.authenticated
    def delete(self, del_id):
        if self.is_admin():
            pass
        else:
            return False
        is_deleted = self.mclass.delete(del_id)
        if is_deleted:
            self.redirect('/maintain/pycatecategory/list')
        else:
            return False
