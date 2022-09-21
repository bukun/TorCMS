# -*- coding:utf-8 -*-
'''
Handler of Pages via Ajax.
'''

import json

import tornado.escape
import tornado.web

from config import CMS_CFG
from torcms.handlers.page_handler import PageHandler
from torcms.model.wiki_model import MWiki
from torcms.model.wiki_hist_model import MWikiHist
from torcms.model.user_model import MUser


class PageAjaxHandler(PageHandler):
    '''
    Handler of Pages via Ajax.
    '''

    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['_add']:
            self.p_to_add()

        elif len(url_arr) == 2:
            if url_arr[0] == 'list':
                self.p_list(url_arr[1])

        elif len(url_arr) == 3:
            self.p_list(url_arr[1], url_arr[2])

        elif len(url_arr) == 1:
            self.view_or_add(url_str)
        else:
            return '{}'

    def post(self, *args, **kwargs):
        '''
        用户操作。
        '''
        _ = kwargs
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_str == 'j_add':
            self.json_add()
        elif url_arr[0] == 'j_edit':
            self.json_edit(url_arr[1])
        # elif url_str == 'j_delete':
        #     self.json_delete()
        elif url_str == 'j_list':
            self.json_list()
        elif url_str == 'j_view':
            self.json_view()

    def view(self, rec):
        '''
        view the post.
        '''
        out_json = {
            'uid': rec.uid,
            'time_update': rec.time_update,
            'title': rec.title,
            'cnt_html': tornado.escape.xhtml_unescape(rec.cnt_html),
        }
        self.write(json.dumps(out_json))

    @tornado.web.authenticated
    def to_add(self, citiao):
        self.write(json.dumps({'code': citiao}))

    def p_list(self, kind, cur_p=''):
        '''
        List the post .
        ToDo: 检查
        '''
        current_page_number = 1
        if cur_p == '':
            current_page_number = 1
        else:
            try:
                current_page_number = int(cur_p)
            except TypeError:
                current_page_number = 1
            except Exception as err:
                print(err.args)
                print(str(err))
                print(repr(err))

        current_page_number = 1 if current_page_number < 1 else current_page_number

        pager_num = int(MWiki.total_number(kind) / CMS_CFG['list_num'])

        kwd = {
            'pager': '',
            'title': 'Recent pages.',
            'kind': kind,
            'current_page': current_page_number,
            'page_count': MWiki.get_counts(),
        }

        self.render('admin/page_ajax/page_list.html',
                    postrecs=MWiki.query_pager_by_kind(
                        kind=kind, current_page_num=current_page_number),
                    kwd=kwd)

    @tornado.web.authenticated
    def p_to_add(self):
        '''
        To add the page.
        '''
        self.render('admin/page_ajax/page_add.html', kwd={})

    @tornado.web.authenticated
    def json_add(self):
        '''
        Add new page.
        '''

        post_data = self.get_request_arguments()

        post_data['user_name'] = 'admin'

        slug = post_data['slug'].strip()
        title = post_data['title'].strip()
        if len(title) < 2:
            output = {
                'info': 'Title cannot be less than 2 characters',
                'code': '0'
            }

            return json.dump(output, self)

        if MWiki.get_by_uid(slug):
            self.set_status(400)
            output = {
                'info': 'slug already exists',
                'code': '-1'
            }

            return json.dump(output, self)
        else:
            MWiki.create_page(slug, post_data)
            tornado.ioloop.IOLoop.instance().add_callback(self.cele_gen_whoosh)
            output = {
                'info': 'Added successfully',
                'code': '1'
            }

            return json.dump(output, self)

    def json_view(self):
        '''
        When access with the slug, It will add the page if there is no record in database.
        '''

        post_data = self.get_request_arguments()
        slug = post_data.get('slug', '')
        print("*" * 50)
        print(slug)
        rec_page = MWiki.get_by_uid(slug)

        if rec_page:
            if rec_page.kind == self.kind:

                out_json = {
                    'code': '1',
                    'info': 'success',
                    'uid': rec_page.uid,
                    'time_update': rec_page.time_update,
                    'title': rec_page.title,
                    'cnt_html': tornado.escape.xhtml_unescape(rec_page.cnt_html),
                    'cnt_md': rec_page.cnt_md
                }

                return json.dump(out_json, self)
            else:
                out_json = {
                    'code': '0',
                    'info': 'Page not found'
                }
                return json.dump(out_json, self)
        else:
            out_json = {
                'code': '-1',
                'info': 'Page not found'
            }
            return json.dump(out_json, self)

    def json_list(self):
        '''
        View the list of the pages.
        '''
        recs = MWiki.query_recent(kind=2)
        rec_arr = []

        for rec in recs:
            rec_arr.append({'title': rec.title, 'slug': rec.uid, 'cnt_md': rec.cnt_md})

        out_json = {
            'code': '1',
            'info': 'success',
            'recs': rec_arr
        }
        return json.dump(out_json, self)

    @tornado.web.authenticated
    def json_edit(self, slug):
        '''
        Update the page.
        '''

        post_data = self.get_request_arguments()

        post_data['user_name'] = 'admin'
        self.userinfo = MUser.get_by_name('admin')
        pageinfo = MWiki.get_by_uid(slug)

        cnt_old = tornado.escape.xhtml_unescape(pageinfo.cnt_md).strip()
        cnt_new = post_data['cnt_md'].strip()
        if cnt_old == cnt_new:
            pass
        else:
            MWikiHist.create_wiki_history(MWiki.get_by_uid(slug),
                                          self.userinfo)

        MWiki.update(slug, post_data)

        # tornado.ioloop.IOLoop.instance().add_callback(self.cele_gen_whoosh)

        out_json = {
            'code': '1',
            'info': 'success',
            'uid': slug
        }
        return json.dump(out_json, self)
