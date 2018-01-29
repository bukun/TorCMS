# -*- coding:utf-8 -*-

'''
History handler for wiki, and page.
'''

import tornado.escape
import tornado.web

from torcms.model.wiki_model import MWiki
from torcms.model.wiki_hist_model import MWikiHist
from torcms.core.tools import diff_table
from .post_history_handler import EditHistoryHander


class WikiHistoryHandler(EditHistoryHander):
    '''
    History handler for wiki, and page.
    '''

    def initialize(self, **kwargs):
        super(WikiHistoryHandler, self).initialize()

    @tornado.web.authenticated
    def update(self, uid):
        '''
        Update the post via ID.
        '''
        if self.userinfo.role[0] > '0':
            pass
        else:
            return False

        post_data = self.get_post_data()
        post_data['user_name'] = self.userinfo.user_name if self.userinfo else ''
        cur_info = MWiki.get_by_uid(uid)
        MWikiHist.create_wiki_history(cur_info)
        MWiki.update_cnt(uid, post_data)
        if cur_info.kind == '1':
            self.redirect('/wiki/{0}'.format(cur_info.title))
        elif cur_info.kind == '2':
            self.redirect('/page/{0}.html'.format(cur_info.uid))

    @tornado.web.authenticated
    def to_edit(self, postid):
        '''
        Try to edit the Post.
        '''
        if self.userinfo.role[0] > '0':
            pass
        else:
            return False
        self.render('man_info/wiki_man_edit.html',
                    userinfo=self.userinfo,
                    postinfo=MWiki.get_by_uid(postid))

    @tornado.web.authenticated
    def delete(self, uid):
        '''
        Delete the history of certain ID.
        '''
        if self.check_post_role()['DELETE']:
            pass
        else:
            return False

        histinfo = MWikiHist.get_by_uid(uid)
        if histinfo:
            pass
        else:
            return False

        postinfo = MWiki.get_by_uid(histinfo.wiki_id)
        MWikiHist.delete(uid)
        self.redirect('/wiki_man/view/{0}'.format(postinfo.uid))

    def view(self, uid):
        '''
        View the wiki with hisotical infos.
        '''
        postinfo = MWiki.get_by_uid(uid)
        if postinfo:
            pass
        else:
            return

        hist_recs = MWikiHist.query_by_wikiid(uid, limit=5)
        html_diff_arr = []
        for hist_rec in hist_recs:

            if hist_rec:
                infobox = diff_table(hist_rec.cnt_md, postinfo.cnt_md)
                hist_user = hist_rec.user_name
                hist_time = hist_rec.time_update

                hist_words_num = len((hist_rec.cnt_md).strip())
                post_words_num = len((postinfo.cnt_md).strip())
                up_words_num = post_words_num - hist_words_num
            else:
                infobox = ''
                hist_user = ''
                hist_time = ''
                up_words_num = ''

            html_diff_arr.append(
                {'hist_uid': hist_rec.uid,
                 'html_diff': infobox,
                 'hist_user': hist_user,
                 'hist_time': hist_time,
                 'up_words_num': up_words_num
                 }
            )

        self.render('man_info/wiki_man_view.html',
                    userinfo=self.userinfo,
                    view=postinfo,  # Deprecated
                    postinfo=postinfo,
                    html_diff_arr=html_diff_arr)

    @tornado.web.authenticated
    def restore(self, hist_uid):
        '''
        Restore by ID
        '''
        if self.check_post_role()['ADMIN']:
            pass
        else:
            return False
        histinfo = MWikiHist.get_by_uid(hist_uid)
        if histinfo:
            pass
        else:
            return False

        postinfo = MWiki.get_by_uid(histinfo.wiki_id)
        cur_cnt = tornado.escape.xhtml_unescape(postinfo.cnt_md)
        old_cnt = tornado.escape.xhtml_unescape(histinfo.cnt_md)

        MWiki.update_cnt(
            histinfo.wiki_id,
            {'cnt_md': old_cnt, 'user_name': self.userinfo.user_name}
        )

        MWikiHist.update_cnt(
            histinfo.uid,
            {'cnt_md': cur_cnt, 'user_name': postinfo.user_name}
        )

        if postinfo.kind == '1':
            self.redirect('/wiki/{0}'.format(postinfo.title))
        elif postinfo.kind == '2':
            self.redirect('/page/{0}.html'.format(postinfo.uid))
