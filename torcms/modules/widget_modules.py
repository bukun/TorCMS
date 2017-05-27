# -*- coding:utf-8 -*-

'''
Define the widget modules for TorCMS.
'''

import tornado.escape
import tornado.web
from torcms.model.reply_model import MReply
from torcms.model.rating_model import MRating
from torcms.core.libs.deprecation import deprecated


class BaiduShare(tornado.web.UIModule):
    '''
    widget for baidu share.
    '''

    def render(self):
        return self.render_string('modules/widget/baidu_share.html')


class ReplyPanel(tornado.web.UIModule):
    '''
    the reply panel.
    '''

    def render(self, *args):
        uid = args[0]
        userinfo = args[1]
        return self.render_string(
            'modules/widget/reply_panel.html',
            uid=uid,
            replys=MReply.query_by_post(uid),
            userinfo=userinfo,
            unescape=tornado.escape.xhtml_unescape,
            linkify=tornado.escape.linkify
        )


class UserinfoWidget(tornado.web.UIModule, tornado.web.RequestHandler):
    '''
    userinfo widget.
    '''

    def render(self, **kwargs):
        is_logged = True if ('userinfo' in kwargs and kwargs['userinfo']) else False
        return self.render_string(
            'modules/widget/loginfo.html',
            userinfo=kwargs['userinfo'],
            is_logged=is_logged)


class WidgetEditor(tornado.web.UIModule):
    '''
    editor widget.
    '''

    def render(self, router, uid, userinfo):
        kwd = {
            'router': router,
            'uid': uid,
        }
        return self.render_string(
            'modules/widget/widget_editor.html',
            kwd=kwd,
            userinfo=userinfo)


class WidgetSearch(tornado.web.UIModule):
    '''
    search widget. Simple searching. searching for all.
    '''

    def render(self):
        # tag_enum = MCategory.query_pcat()
        return self.render_string('modules/widget/widget_search.html')


class StarRating(tornado.web.UIModule):
    '''
    For rating of posts.
    '''

    def render(self, postinfo, userinfo):
        rating = False
        if userinfo:
            rating = MRating.get_rating(postinfo.uid, userinfo.uid)
        if rating:
            pass
        else:
            rating = postinfo.rating
        return self.render_string(
            'modules/widget/star_rating.html',
            unescape=tornado.escape.xhtml_unescape,
            postinfo=postinfo,
            userinfo=userinfo,
            rating=rating,
        )


class NavigatePanel(tornado.web.UIModule):
    '''
    render navigate panel.
    '''

    @deprecated(details='Should not used any more.')
    def render(self, userinfo):
        return self.render_string(
            'modules/widget/navigate_panel.html',
            unescape=tornado.escape.xhtml_unescape,
            userinfo=userinfo,
        )


class FooterPanel(tornado.web.UIModule):
    '''
    render footer panel.
    '''

    @deprecated(details='Should not used any more.')
    def render(self, userinfo):
        return self.render_string(
            'modules/widget/footer_panel.html',
            unescape=tornado.escape.xhtml_unescape,
            userinfo=userinfo,
        )


class UseF2E(tornado.web.UIModule):
    '''
    using f2e lib.
    '''

    def render(self, f2ename):
        return self.render_string(
            'modules/usef2e/{0}.html'.format(f2ename),
        )


class BaiduSearch(tornado.web.UIModule):
    '''
    widget for baidu search.
    '''

    def render(self, ):
        baidu_script = ''
        return self.render_string('modules/info/baidu_script.html',
                                  baidu_script=baidu_script)
