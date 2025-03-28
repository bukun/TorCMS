# -*- coding:utf-8 -*-
'''
Manage the posts by Administrator.
'''

from abc import ABCMeta, abstractmethod

import tornado.escape
import tornado.web

import config
from config import post_cfg
from torcms.core import privilege
from torcms.core.base_handler import BaseHandler
from torcms.core.tools import diff_table
from torcms.model.post_hist_model import MPostHist
from torcms.model.post_model import MPost
from torcms.model.staff2role_model import MStaff2Role


class EditHistoryHander(BaseHandler):
    '''
    Manage the posts by Administrator.
    '''

    __metaclass__ = ABCMeta

    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):
        url_arr = self.parse_url(args[0])

        dict_get = {
            'view': self.view,
            'edit': self.to_edit,
            'restore': self.restore,
            'delete': self.delete,
        }

        if len(url_arr) == 2:
            dict_get.get(url_arr[0])(url_arr[1])
        else:
            self.show404()

            # if url_arr[0] == 'view':
            #     self.view(url_arr[1])
            # elif url_arr[0] == 'edit':
            #     self.to_edit(url_arr[1])
            # elif url_arr[0] == 'restore':
            #     self.restore(url_arr[1])
            # elif url_arr[0] == 'delete':
            #     self.delete(url_arr[1])
            # else:
            #     kwd = {
            #         'info': '页面未找到',
            #     }
            #     self.render('misc/html/404.html',
            #                 kwd=kwd,
            #                 userinfo=self.userinfo)

    def post(self, *args, **kwargs):
        url_arr = self.parse_url(args[0])

        if url_arr[0] == 'edit':
            self.update(url_arr[1])
        else:
            self.show404()

    @abstractmethod
    def update(self, uid):
        '''
        update by buid
        '''
        return

    @abstractmethod
    def to_edit(self, postid):
        '''
        to edit
        '''
        return

    # @abstractmethod
    # def __could_edit(self, postid):
    #     '''
    #     check if the post could edit.
    #     :param postid:
    #     :return:
    #     '''
    #     return

    @abstractmethod
    def delete(self, uid):
        '''
        delete the post.
        '''
        return

    @abstractmethod
    def view(self, uid):
        '''
        view the post
        '''
        return

    @abstractmethod
    def restore(self, hist_uid):
        '''
        restore the history
        '''
        return


class PostHistoryHandler(EditHistoryHander):
    '''
    Manage the posts by Administrator.
    '''

    def initialize(self):
        super().initialize()

    @tornado.web.authenticated
    @privilege.permission(action='can_review')
    def update(self, uid):
        post_data = self.get_request_arguments()
        if self.userinfo:
            post_data['user_name'] = self.userinfo.user_name
        else:
            post_data['user_name'] = ''
        cur_info = MPost.get_by_uid(uid)
        cur_info.user_name = post_data['user_name']

        cnt_old = tornado.escape.xhtml_unescape(cur_info.cnt_md).strip()
        cnt_new = post_data['cnt_md'].strip()
        if cnt_old == cnt_new:
            pass
        else:
            MPostHist.create_post_history(cur_info, self.userinfo)
            MPost.update_cnt(uid, post_data)
        self.redirect('/{0}/{1}'.format(post_cfg[cur_info.kind]['router'], uid))

    @tornado.web.authenticated
    @privilege.permission(action='can_review')
    def to_edit(self, postid):
        post_rec = MPost.get_by_uid(postid)
        kwd = {}
        self.render(
            'man_info/post_man_edit.html',
            userinfo=self.userinfo,
            postinfo=post_rec,
            kwd=kwd,
        )

    @tornado.web.authenticated
    @privilege.permission(action='can_review')
    def __could_edit(self, postid):
        post_rec = MPost.get_by_uid(postid)
        if not post_rec:
            return False
        if post_rec.user_name == self.userinfo.user_name:
            return True
        else:
            return False

    @tornado.web.authenticated
    @privilege.permission(action='can_review')
    def delete(self, uid):
        histinfo = MPostHist.get_by_uid(uid)
        if histinfo:
            pass
        else:
            return False

        postinfo = MPost.get_by_uid(histinfo.post_id)
        MPostHist.delete(uid)

        self.redirect('/post_man/view/{0}'.format(postinfo.uid))

    @tornado.web.authenticated
    @privilege.permission(action='can_review')
    def view(self, uid):
        postinfo = MPost.get_by_uid(uid)
        if postinfo:
            pass
        else:
            return
        kwd = {}
        hist_recs = MPostHist.query_by_postid(uid, limit=5)
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
        if self.userinfo:
            kwd['can_review'] = MStaff2Role.check_permissions(
                self.userinfo.uid, 'can_review'
            )

        self.render(
            'man_info/post_man_view.html',
            userinfo=self.userinfo,
            view=postinfo,
            postinfo=postinfo,
            html_diff_arr=html_diff_arr,
            router=post_cfg[postinfo.kind]['router'],
            kwd=kwd,
        )

    @tornado.web.authenticated
    @privilege.permission(action='can_review')
    def restore(self, hist_uid):
        histinfo = MPostHist.get_by_uid(hist_uid)
        if histinfo:
            pass
        else:
            return False

        postinfo = MPost.get_by_uid(histinfo.post_id)
        cur_cnt = tornado.escape.xhtml_unescape(postinfo.cnt_md)
        old_cnt = tornado.escape.xhtml_unescape(histinfo.cnt_md)

        MPost.update_cnt(
            histinfo.post_id, {'cnt_md': old_cnt, 'user_name': self.userinfo.user_name}
        )

        MPostHist.update_cnt(
            histinfo.uid, {'cnt_md': cur_cnt, 'user_name': postinfo.user_name}
        )
        self.redirect(
            '/{0}/{1}'.format(post_cfg[postinfo.kind]['router'], postinfo.uid)
        )
