# -*- coding:utf-8 -*-

import tornado.escape
import tornado.web
from torcms.core.base_handler import BaseHandler
from torcms.model.wiki_model import MWiki
from torcms.model.wiki_hist_model import MWikiHist
from torcms.core.tools import diff_table


class WikiManHandler(BaseHandler):
    def initialize(self):
        super(WikiManHandler, self).initialize()
        self.mpost = MWiki()
        self.mposthist = MWikiHist()

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
        if cur_info.kind == '1':
            self.redirect('/wiki/{0}'.format(cur_info.title))
        elif cur_info.kind == '2':
            self.redirect('/page/{0}.html'.format(cur_info.uid))

    @tornado.web.authenticated
    def to_edit(self, postid):
        if self.userinfo.role[0] > '0':
            pass
        else:
            return False
        post_rec = self.mpost.get_by_uid(postid)
        self.render('man_wiki/wiki_man_edit.html',
                    userinfo=self.userinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    postinfo=post_rec,
                    )

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

        postinfo = self.mpost.get_by_id(histinfo.wiki_id)
        self.mposthist.delete(uid)
        self.redirect('/wiki_man/view/{0}'.format(postinfo.uid))

    def view(self, uid):
        postinfo = self.mpost.get_by_id(uid)
        if postinfo:
            pass
        else:
            return

        hist_recs = self.mposthist.query_by_wikiid(uid, limit=5)
        html_diff_arr = []
        for hist_rec in hist_recs:

            if hist_rec:
                infobox = diff_table(hist_rec.cnt_md, postinfo.cnt_md)
            else:
                infobox = ''

            html_diff_arr.append({'hist_uid': hist_rec.uid, 'html_diff': infobox})

        self.render('man_wiki/wiki_man_view.html',
                    userinfo=self.userinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    view=postinfo,  # Deprecated
                    postinfo=postinfo,
                    html_diff_arr=html_diff_arr
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

        postinfo = self.mpost.get_by_id(histinfo.wiki_id)
        cur_cnt = tornado.escape.xhtml_unescape(postinfo.cnt_md)
        old_cnt = tornado.escape.xhtml_unescape(histinfo.cnt_md)

        self.mpost.update_cnt(histinfo.wiki_id,
                              {'cnt_md': old_cnt, 'user_name': self.userinfo.user_name}
                              )

        self.mposthist.update_cnt(histinfo.uid,
                                  {'cnt_md': cur_cnt, 'user_name': postinfo.user_name}
                                  )

        if postinfo.kind == '1':
            self.redirect('/wiki/{0}'.format(postinfo.title))
        elif postinfo.kind == '2':
            self.redirect('/page/{0}.html'.format(postinfo.uid))
