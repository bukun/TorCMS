# -*- coding:utf-8 -*-

'''
Manage the posts by Administrator.
'''

import tornado.escape
import tornado.web
from config import router_post
from torcms.core.base_handler import BaseHandler
from torcms.model.post_model import MPost
from torcms.model.post_hist_model import MPostHist
from torcms.core.tools import diff_table


class PostManHandler(BaseHandler):
    '''
    Manage the posts by Administrator.
    '''

    def initialize(self):
        super(PostManHandler, self).initialize()
        self.mpost = MPost()
        self.mposthist = MPostHist()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)
        if url_arr[0] == 'view':
            self.view(url_arr[1])
        elif url_arr[0] == 'edit':
            self.to_edit(url_arr[1])
        elif url_arr[0] == 'restore':
            self.restore(url_arr[1])
        elif url_arr[0] == 'delete':
            self.delete(url_arr[1])
        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo, )

    def post(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_arr[0] == 'edit':
            self.update(url_arr[1])
        else:
            self.redirect('html/404.html')

    @tornado.web.authenticated
    def update(self, uid):
        if self.userinfo.role[0] > '0':
            pass
        else:
            return False
        post_data = self.get_post_data()
        if self.userinfo:
            post_data['user_name'] = self.userinfo.user_name
        else:
            post_data['user_name'] = ''
        cur_info = self.mpost.get_by_id(uid)
        self.mposthist.insert_data(cur_info)
        self.mpost.update_cnt(uid, post_data)
        self.redirect('/{0}/{1}'.format(router_post[cur_info.kind], uid))

    @tornado.web.authenticated
    def to_edit(self, postid):
        if self.userinfo.role[0] > '0':
            pass
        else:
            return False
        post_rec = self.mpost.get_by_uid(postid)
        self.render('man_post/post_man_edit.html',
                    userinfo=self.userinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    postinfo=post_rec,
                    )

    @tornado.web.authenticated
    def __could_edit(self, postid):
        post_rec = self.mpost.get_by_uid(postid)
        if not post_rec:
            return False
        if self.check_post_role(self.userinfo)['EDIT'] or post_rec.user_name == self.userinfo.user_name:
            return True
        else:
            return False

    @tornado.web.authenticated
    def delete(self, uid):
        if self.check_post_role(self.userinfo)['DELETE']:
            pass
        else:
            return False

        histinfo = self.mposthist.get_by_id(uid)
        if histinfo:
            pass
        else:
            return False

        postinfo = self.mpost.get_by_id(histinfo.post_id)
        self.mposthist.delete(uid)
        self.redirect('/post_man/view/{0}'.format(postinfo.uid))

    def view(self, uid):
        postinfo = self.mpost.get_by_id(uid)
        if postinfo:
            pass
        else:
            return

        hist_recs = self.mposthist.query_by_postid(uid, limit=5)
        html_diff_arr = []
        for hist_rec in hist_recs:
            if hist_rec:
                infobox = diff_table(hist_rec.cnt_md, postinfo.cnt_md)
            else:
                infobox = ''

            html_diff_arr.append({'hist_uid': hist_rec.uid, 'html_diff': infobox})

        self.render('man_post/post_man_view.html',
                    userinfo=self.userinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    view=postinfo,
                    postinfo=postinfo,
                    html_diff_arr=html_diff_arr,
                    router=router_post[postinfo.kind],
                    )

    @tornado.web.authenticated
    def restore(self, hist_uid):
        if self.check_post_role(self.userinfo)['ADMIN']:
            pass
        else:
            return False
        histinfo = self.mposthist.get_by_id(hist_uid)
        if histinfo:
            pass
        else:
            return False

        postinfo = self.mpost.get_by_id(histinfo.post_id)
        cur_cnt = tornado.escape.xhtml_unescape(postinfo.cnt_md)
        old_cnt = tornado.escape.xhtml_unescape(histinfo.cnt_md)

        self.mpost.update_cnt(histinfo.post_id, {'cnt_md': old_cnt, 'user_name': self.userinfo.user_name})

        self.mposthist.update_cnt(histinfo.uid, {'cnt_md': cur_cnt, 'user_name': postinfo.user_name})
        self.redirect('/{0}/{1}'.format(router_post[postinfo.kind], postinfo.uid))
