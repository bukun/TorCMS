# -*- coding:utf-8 -*-
'''
History handler for wiki, and page.
'''

import tornado.escape
import tornado.web
import config
from torcms.core import privilege
from torcms.core.tools import diff_table
from torcms.model.wiki_hist_model import MWikiHist
from torcms.model.wiki_model import MWiki
from torcms.model.staff2role_model import MStaff2Role
from .post_history_handler import EditHistoryHander


class WikiHistoryHandler(EditHistoryHander):
    '''
    History handler for wiki, and page.
    '''

    def initialize(self, **kwargs):
        super().initialize()
        self.kind = kwargs.get('kind', '1')

    @privilege.permission(action='can_role')
    @tornado.web.authenticated
    def update(self, uid):
        '''
        Update the post via ID.
        '''

        post_data = self.get_request_arguments()
        post_data['user_name'] = self.userinfo.user_name if self.userinfo else ''
        cur_info = MWiki.get_by_uid(uid)

        cnt_old = tornado.escape.xhtml_unescape(cur_info.cnt_md).strip()
        cnt_new = post_data['cnt_md'].strip()
        if cnt_old == cnt_new:
            pass
        else:
            MWikiHist.create_wiki_history(cur_info, self.userinfo)
            MWiki.update_cnt(uid, post_data)
        if cur_info.kind == '1':
            self.redirect('/wiki/{0}'.format(cur_info.title))
        elif cur_info.kind == '2':
            self.redirect('/page/{0}.html'.format(cur_info.uid))

    @privilege.permission(action='can_role')
    @tornado.web.authenticated
    def to_edit(self, postid):
        '''
        Try to edit the Post.
        '''

        kwd = {}
        self.render(
            'man_info/wiki_man_edit.html',
            userinfo=self.userinfo,
            postinfo=MWiki.get_by_uid(postid),
            kwd=kwd,
        )

    @privilege.permission(action='can_role')
    @tornado.web.authenticated
    def delete(self, uid):
        '''
        Delete the history of certain ID.
        '''

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
        if hist_recs:

            for hist_rec in hist_recs:
                infobox = diff_table(hist_rec.cnt_md, postinfo.cnt_md)
                hist_user = hist_rec.user_name
                hist_time = hist_rec.time_update

                hist_words_num = len((hist_rec.cnt_md).strip())
                post_words_num = len((postinfo.cnt_md).strip())
                up_words_num = post_words_num - hist_words_num

                html_diff_arr.append(
                    {
                        'hist_uid': hist_rec.uid,
                        'html_diff': infobox,
                        'hist_user': hist_user,
                        'hist_time': hist_time,
                        'up_words_num': up_words_num,
                    }
                )

        kwd = {}
        if self.userinfo:
            kwd['can_review'] = MStaff2Role.check_permissions(self.userinfo.uid, 'can_review')
            kwd['can_edit'] = MStaff2Role.check_permissions(self.userinfo.uid, 'can_edit')
        self.render(
            'man_info/wiki_man_view.html',
            userinfo=self.userinfo,
            postinfo=postinfo,
            html_diff_arr=html_diff_arr,
            kwd=kwd,
        )

    @privilege.permission(action='can_role')
    @tornado.web.authenticated
    def restore(self, hist_uid):
        '''
        Restore by ID
        '''

        histinfo = MWikiHist.get_by_uid(hist_uid)
        if histinfo:
            pass
        else:
            return False

        postinfo = MWiki.get_by_uid(histinfo.wiki_id)
        cur_cnt = tornado.escape.xhtml_unescape(postinfo.cnt_md)
        old_cnt = tornado.escape.xhtml_unescape(histinfo.cnt_md)

        MWiki.update_cnt(
            histinfo.wiki_id, {'cnt_md': old_cnt, 'user_name': self.userinfo.user_name}
        )

        MWikiHist.update_cnt(
            histinfo.uid, {'cnt_md': cur_cnt, 'user_name': postinfo.user_name}
        )

        if postinfo.kind == '1':
            self.redirect('/wiki/{0}'.format(postinfo.title))
        elif postinfo.kind == '2':
            self.redirect('/page/{0}.html'.format(postinfo.uid))
