# -*- coding:utf-8 -*-
'''
Handler for links.
'''

import json

import tornado.web

from config import CMS_CFG
from torcms.core import privilege, tools
from torcms.core.base_handler import BaseHandler
from torcms.model.link_model import MLink


class LinkHandler(BaseHandler):
    '''
    Handler for links.
    '''

    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_str in ['add_link', '_add', 'add']:
            self.to_add_link()
        elif url_str == 'list':
            self.recent()
        elif url_arr[0] in ['modify', '_edit', 'edit']:
            self.to_modify(url_arr[1])
        elif url_arr[0] in ['delete', '_delete']:
            self.delete_by_id(url_arr[1])
        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render(
                'misc/html/404.html',
                kwd=kwd,
                userinfo=self.userinfo,
            )

    def post(self, *args, **kwargs):
        url_str = args[0]

        if url_str == '':
            return
        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['modify', '_edit', 'edit']:
            self.update(url_arr[1])

        elif url_arr[0] in ['add_link', '_add', 'add']:
            self.p_user_add_link()
        else:
            self.redirect('misc/html/404.html')

    @privilege.permission(action='assign_role')
    @tornado.web.authenticated
    def recent(self):
        '''
        Recent links.
        '''
        kwd = {
            'pager': '',
            'title': '最近文档',
        }

        if self.is_p:
            self.render(
                'admin/link_ajax/link_list.html',
                kwd=kwd,
                view=MLink.query_link(20),
                format_date=tools.format_date,
                userinfo=self.userinfo,
            )
        else:
            self.render(
                'misc/link/link_list.html',
                kwd=kwd,
                view=MLink.query_link(20),
                format_date=tools.format_date,
                userinfo=self.userinfo,
            )

    @privilege.permission(action='assign_role')
    @tornado.web.authenticated
    def to_add_link(
        self,
    ):
        '''
        To add link
        '''

        kwd = {
            'pager': '',
            'uid': '',
        }
        self.render(
            'misc/link/link_add.html',
            topmenu='',
            kwd=kwd,
            userinfo=self.userinfo,
        )

    @privilege.permission(action='assign_role')
    @tornado.web.authenticated
    def update(self, uid):
        '''
        Update the link.
        '''

        post_data = self.get_request_arguments()

        post_data['user_name'] = self.get_current_user()

        if self.is_p:
            if MLink.update(uid, post_data):
                output = {
                    'addinfo ': 1,
                }
            else:
                output = {
                    'addinfo ': 0,
                }
            return json.dump(output, self)
        else:
            if MLink.update(uid, post_data):
                self.redirect('/link/list')

    @privilege.permission(action='assign_role')
    @tornado.web.authenticated
    def to_modify(self, uid):
        '''
        Try to edit the link.
        '''

        self.render(
            'misc/link/link_edit.html',
            kwd={},
            postinfo=MLink.get_by_uid(uid),
            userinfo=self.userinfo,
        )

    @privilege.permission(action='assign_role')
    @tornado.web.authenticated
    def viewit(self, post_id):
        '''
        View the link.
        '''

        rec = MLink.get_by_uid(post_id)

        if not rec:
            kwd = {'info': '您要找的分类不存在。'}
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)
            return False

        kwd = {
            'pager': '',
        }

        self.render(
            'misc/link/link_view.html',
            view=rec,
            kwd=kwd,
            userinfo=self.userinfo,
            cfg=CMS_CFG,
        )

    @privilege.permission(action='assign_role')
    @tornado.web.authenticated
    def p_user_add_link(self):
        '''
        user add link.
        '''

        post_data = self.get_request_arguments()

        post_data['user_name'] = self.get_current_user()

        cur_uid = tools.get_uudd(2)
        while MLink.get_by_uid(cur_uid):
            cur_uid = tools.get_uudd(2)

        if MLink.create_link(cur_uid, post_data):
            output = {
                'addinfo ': 1,
            }
        else:
            output = {
                'addinfo ': 0,
            }
        return json.dump(output, self)

    @privilege.permission(action='assign_role')
    @tornado.web.authenticated
    def user_add_link(self):
        '''
        Create link by user.
        '''

        post_data = self.get_request_arguments()

        post_data['user_name'] = self.get_current_user()

        cur_uid = tools.get_uudd(2)
        while MLink.get_by_uid(cur_uid):
            cur_uid = tools.get_uudd(2)

        MLink.create_link(cur_uid, post_data)

        self.redirect('/link/list')

    @privilege.permission(action='assign_role')
    @tornado.web.authenticated
    def delete_by_id(self, del_id):
        '''
        Delete a link by id.
        '''

        if self.is_p:
            if MLink.delete(del_id):
                output = {'del_link': 1}
            else:
                output = {'del_link': 0}
            return json.dump(output, self)
        else:
            is_deleted = MLink.delete(del_id)
            if is_deleted:
                self.redirect('/link/list')


class LinkPartialHandler(LinkHandler):
    '''
    Partially render for user handler.
    '''

    def initialize(self, **kwargs):
        super().initialize()
        self.is_p = True
