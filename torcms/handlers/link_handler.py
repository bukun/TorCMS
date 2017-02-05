# -*- coding:utf-8 -*-

import json
import tornado.escape
import tornado.web
import config
from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.link_model import MLink


class LinkHandler(BaseHandler):
    def initialize(self):
        super(LinkHandler, self).initialize()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_str in ['add_link', '_add', 'add']:
            self.to_add_link()
        elif url_str == 'list':
            self.recent()
        elif url_arr[0] in ['modify', '_edit', 'edit']:
            self.to_modify(url_arr[1])
        elif url_arr[0] in ['delete', '_delete']:
            self.delete(url_arr[1])
        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )

    def post(self, url_str=''):
        if url_str == '':
            return
        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['modify', '_edit', 'edit']:
            self.update(url_arr[1])

        elif url_arr[0] in ['add_link', '_add', 'add']:
            self.p_user_add_link()
        else:
            self.redirect('html/404.html')

    def recent(self):
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': '最近文档',
        }
        self.render('doc/link/link_list.html',
                    kwd=kwd,
                    view=MLink.query_link(10),
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    )

    def to_add_link(self, ):
        if self.check_post_role()['ADD']:
            pass
        else:
            return False
        kwd = {
            'pager': '',
            'uid': '',
        }
        self.render('doc/link/link_add.html',
                    topmenu='',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    )

    @tornado.web.authenticated
    def update(self, uid):
        if self.userinfo.role[1] >= '3':
            pass
        else:
            return False
        post_data = self.get_post_data()

        post_data['user_name'] = self.get_current_user()

        if MLink.update(uid, post_data):
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
        if self.userinfo.role[1] >= '3':
            pass
        else:
            return False
        a = MLink.get_by_uid(id_rec)

        self.render('doc/link/link_edit.html',
                    kwd={},
                    unescape=tornado.escape.xhtml_unescape,
                    dbrec=a,
                    userinfo=self.userinfo)

    @tornado.web.authenticated
    def viewit(self, post_id):

        rec = MLink.get_by_uid(post_id)

        if not rec:
            kwd = {'info': '您要找的分类不存在。'}
            self.render('html/404.html', kwd=kwd)
            return False

        kwd = {
            'pager': '',
            'editable': self.editable(),
        }

        self.render('doc/link/link_view.html',
                    view=rec,
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    userinfo=self.userinfo,
                    cfg=config.CMS_CFG,
                    )

    @tornado.web.authenticated
    def p_user_add_link(self):

        if self.check_post_role()['ADD']:
            pass
        else:
            return False
        post_data = self.get_post_data()

        post_data['user_name'] = self.get_current_user()

        cur_uid = tools.get_uudd(2)
        while MLink.get_by_uid(cur_uid):
            cur_uid = tools.get_uudd(2)

        if MLink.create_wiki_history(cur_uid, post_data):
            output = {
                'addinfo ': 1,
            }
        else:
            output = {
                'addinfo ': 0,
            }
        return json.dump(output, self)

    @tornado.web.authenticated
    def user_add_link(self):

        if self.check_post_role()['ADD']:
            pass
        else:
            return False
        post_data = self.get_post_data()

        post_data['user_name'] = self.get_current_user()

        cur_uid = tools.get_uudd(2)
        while MLink.get_by_uid(cur_uid):
            cur_uid = tools.get_uudd(2)

        MLink.create_wiki_history(cur_uid, post_data)

        self.redirect('/link/list')

    @tornado.web.authenticated
    def delete(self, del_id):
        if self.check_post_role()['DELETE']:
            pass
        else:
            return False

        if MLink.delete(del_id):
            output = {'del_link': 1}
        else:
            output = {'del_link': 0}
        return json.dump(output, self)
