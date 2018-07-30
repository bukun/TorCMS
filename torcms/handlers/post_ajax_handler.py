# -*- coding:utf-8 -*-

'''
Handler of Posts via Ajax.
'''

import json
import tornado.web
import tornado.escape
from torcms.handlers.post_handler import PostHandler
from torcms.model.post_model import MPost
from config import CMS_CFG
from torcms.core import tools


class PostAjaxHandler(PostHandler):
    '''
    Handler of Posts via Ajax.
    '''

    def initialize(self, **kwargs):
        super(PostAjaxHandler, self).initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(args[0])
        if url_arr[0] in ['_delete', 'delete']:
            self.j_delete(url_arr[1])
        elif url_arr[0] in ['count_plus']:
            self.count_plus(url_arr[1])

        if len(url_arr) == 2:
            if url_arr[0] == 'recent':
                self.p_recent(url_arr[1])

        elif len(url_arr) == 3:
            self.p_recent(url_arr[1], url_arr[2])

        elif len(url_arr) == 1 and len(url_str) in [4, 5]:
            self._view_or_add(url_str)

    def viewinfo(self, postinfo):
        '''
        View the info
        '''
        out_json = {
            'uid': postinfo.uid,
            'time_update': postinfo.time_update,
            'title': postinfo.title,
            'cnt_html': tornado.escape.xhtml_unescape(postinfo.cnt_html),

        }
        self.write(json.dumps(out_json))

    def count_plus(self, uid):
        '''
        Ajax request, that the view count will plus 1.
        '''
        self.set_header("Content-Type", "application/json")
        output = {
            # ToDo: Test the following codes.
            # MPost.__update_view_count_by_uid(uid) else 0,
            'status': 1 if MPost.update_misc(uid, count=1) else 0
        }
        # return json.dump(output, self)
        self.write(json.dumps(output))

    def p_recent(self, kind, cur_p='', with_catalog=True, with_date=True):
        '''
        List posts that recent edited, partially.
        '''
        if cur_p == '':
            current_page_number = 1
        else:
            current_page_number = int(cur_p)

        current_page_number = 1 if current_page_number < 1 else current_page_number

        pager_num = int(MPost.total_number(kind) / CMS_CFG['list_num'])
        kwd = {
            'pager': '',
            'title': 'Recent posts.',
            'with_catalog': with_catalog,
            'with_date': with_date,
            'kind': kind,
            'current_page': current_page_number,
            'post_count': MPost.get_counts(),
        }
        self.render('admin/post_ajax/post_list.html',
                    kwd=kwd,
                    view=MPost.query_recent(num=20, kind=kind),
                    infos=MPost.query_pager_by_slug(
                        kind=kind,
                        current_page_num=current_page_number
                    ),
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    cfg=CMS_CFG, )
