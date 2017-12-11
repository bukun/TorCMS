# -*- coding:utf-8 -*-

'''
CRUD for the category.
'''

import json
import tornado.escape
import tornado.web
import config
from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.category_model import MCategory


class MaintainCategoryHandler(BaseHandler):
    '''
    CRUD for the category.
    '''

    def initialize(self, **kwargs):
        super(MaintainCategoryHandler, self).initialize(kwargs)
        self.tmpl_router = 'maintain_category'

    def get(self, *args, **kwargs):
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

    def post(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        if url_arr[0] == 'modify':
            self.update(url_arr[1])
        elif url_str == 'add':
            self.p_add_category()
        elif url_arr[0] == 'add':

            self.p_add_category()
        else:
            self.redirect('misc/html/404.html')

    def list_catalog(self):
        '''
        listing the category.
        '''
        kwd = {
            'pager': '',
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
        '''
        Adding the category
        '''
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

        return False

    @tornado.web.authenticated
    def update(self, uid):
        '''
        Updating the category.
        '''
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
        '''
        to edit the category by ID.
        :param id_rec:  post ID
        '''
        if self.__could_edit(id_rec):
            pass
        else:
            return False
        category_rec = MCategory.get_by_uid(id_rec)

        if category_rec:
            pass
        else:
            return None
        kwd = {
            'pager': '',

        }
        self.render('admin/{0}/category_edit.html'.format(self.tmpl_router),
                    kwd=kwd,
                    postinfo=category_rec,
                    userinfo=self.userinfo,
                    cfg=config.CMS_CFG)

    @tornado.web.authenticated
    def p_add_category(self):
        '''
        Adding the category
        '''
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
        '''
        Adding the category
        '''
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

        MCategory.add_or_update(cur_uid, post_data)

        self.redirect('/maintain/category/list')

    @tornado.web.authenticated
    def delete_by_uid(self, del_id):
        '''
        Deleting the category via ID.
        '''
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
    '''
    CRUD for the category. By AJAX.
    '''

    def initialize(self, **kwargs):
        super(MaintainCategoryAjaxHandler, self).initialize(kwargs)
        self.tmpl_router = 'category_ajax'
