# -*- coding:utf-8 -*-

'''
Define the widget modules for TorCMS.
'''
import tornado.escape
import tornado.web

import config
from torcms.model.category_model import MCategory
from torcms.model.rating_model import MRating
from torcms.model.reply_model import MReply
from torcms.model.replyid_model import MReplyid
from torcms.model.user_model import MUser


class BaiduShare(tornado.web.UIModule):
    '''
    widget for baidu share.
    '''

    def render(self, *args, **kwargs):
        en = kwargs.get('en', False)
        return self.render_string('modules/widget/baidu_share.html', en=en)


class ReplyPanel(tornado.web.UIModule):
    '''
    the reply panel.
    '''

    def render(self, *args, **kwargs):
        uid = args[0]
        userinfo = args[1]

        return self.render_string(
            'modules/widget/reply_panel.html',
            uid=uid,
            replys=MReply.query_by_post(uid),
            userinfo=userinfo,
            linkify=tornado.escape.linkify
        )


class UserinfoWidget(tornado.web.UIModule, tornado.web.RequestHandler):
    '''
    userinfo widget.
    '''

    def render(self, *args, **kwargs):
        # is_logged = kwargs.get('userinfo', False)
        is_logged = True if ('userinfo' in kwargs and kwargs['userinfo']) else False
        return self.render_string(
            'modules/widget/loginfo.html',
            userinfo=kwargs['userinfo'],
            is_logged=is_logged)


class WidgetEditor(tornado.web.UIModule):
    '''
    editor widget.
    '''

    def render(self, *args, **kwargs):
        router = args[0]
        uid = args[1]
        userinfo = args[2]
        review = kwargs.get('review', True)
        delete = kwargs.get('delete', False)
        nullify = kwargs.get('nullify', False)
        reclass = kwargs.get('reclass', True)
        url = kwargs.get('url', '')
        if 'catid' in kwargs:
            catid = kwargs['catid']
        else:
            catid = ''
        kwd = {
            'router': router,
            'uid': uid,
            'catid': catid,
            'review': review,
            'delete': delete,
            'nullify': nullify,
            'reclass': reclass,
            'url': url

        }
        return self.render_string(
            'modules/widget/widget_editor.html',
            kwd=kwd,
            userinfo=userinfo)


class WidgetSearch(tornado.web.UIModule):
    '''
    search widget. Simple searching. searching for all.
    '''

    def render(self, *args, **kwargs):
        # tag_enum = MCategory.query_pcat()
        return self.render_string('modules/widget/widget_search.html')


class StarRating(tornado.web.UIModule):
    '''
    For rating of posts.
    '''

    def render(self, *args, **kwargs):
        postinfo = args[0]
        userinfo = args[1]
        rating = False
        if userinfo:
            rating = MRating.get_rating(postinfo.uid, userinfo.uid)
        if rating:
            pass
        else:
            rating = postinfo.rating
        return self.render_string(
            'modules/widget/star_rating.html',

            postinfo=postinfo,
            userinfo=userinfo,
            rating=rating,
        )


class UseF2E(tornado.web.UIModule):
    '''
    using f2e lib.
    '''

    def render(self, *args, **kwargs):
        f2ename = args[0]
        return self.render_string(
            'modules/usef2e/{0}.html'.format(f2ename)
        )


class BaiduSearch(tornado.web.UIModule):
    '''
    widget for baidu search.
    '''

    def render(self, *args, **kwargs):
        baidu_script = ''
        return self.render_string('modules/info/baidu_script.html',
                                  baidu_script=baidu_script)


class UploadPicture(tornado.web.UIModule):
    '''
    Upload picture
    '''

    def render(self, *args, **kwargs):
        return self.render_string('modules/widget/upload_entity_pic.html')


class UploadFile(tornado.web.UIModule):
    '''
    Upload file
    '''

    def render(self, *args, **kwargs):
        return self.render_string('modules/widget/upload_entity_file.html')


class Navigation_menu(tornado.web.UIModule):
    '''
    Web site secondary navigation
    '''

    def render(self, *args, **kwargs):
        kind = args[0]

        title = kwargs.get('title', '')
        filter_view = kwargs.get('filter_view', False)
        slug = kwargs.get('slug', False)
        curinfo = MCategory.query_kind_cat(kind)

        kwd = {
            'title': title,
            'router': config.router_post[kind],
            'kind': kind,
            'filter_view': filter_view,
            'slug': slug
        }

        return self.render_string('modules/widget/nav_menu.html',
                                  pcatinfo=curinfo,
                                  kwd=kwd)


class CommentList(tornado.web.UIModule):
    '''
    reply list
    '''

    def render(self, *args, **kwargs):
        replyid = kwargs.get('replyid', '')
        userinfo = kwargs.get('userinfo', '')
        res = MReplyid.get_by_rid(replyid)
        datas = []
        for x in res:
            rec = MReply.get_by_uid(x.reply1)
            if rec in datas:
                pass
            else:
                datas.append(rec)
        return self.render_string('modules/widget/comment_list.html',
                                  userinfo=userinfo,
                                  recs=datas
                                  )


class Replycnt(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        replyid = kwargs.get('replyid', '')
        res = MReply.get_by_uid(replyid)
        reply_cnt = res.cnt_md
        return reply_cnt


class Userprofile(tornado.web.UIModule):
    '''
    the reply panel.
    '''

    def render(self, *args, **kwargs):
        user_id = args[0]
        rec = MUser.get_by_uid(user_id)

        return self.render_string('modules/user_profile.html',
                                  rec=rec)
