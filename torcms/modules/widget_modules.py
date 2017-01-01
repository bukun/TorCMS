# -*- coding:utf-8 -*-

import tornado.escape
import tornado.web
import tornado.web
from torcms.model.category_model import MCategory


from torcms.model.reply_model import MReply
from torcms.model.page_model import MPage
from torcms.model.rating_model import MRating

mreply = MReply()
mpage = MPage()
mrating = MRating()


class baidu_share(tornado.web.UIModule):
    def render(self):
        return self.render_string('modules/widget/baidu_share.html')

class reply_panel(tornado.web.UIModule):
    def render(self, uid, userinfo):
        return self.render_string('modules/widget/reply_panel.html',
                                  uid=uid,
                                  replys=mreply.query_by_post(uid),
                                  userinfo=userinfo,
                                  unescape=tornado.escape.xhtml_unescape,
                                  linkify=tornado.escape.linkify,
                                  )


class userinfo_widget(tornado.web.UIModule, tornado.web.RequestHandler):
    def render(self, signature):
        if self.get_secure_cookie("user"):
            self.render('modules/widget/loginfo.html',
                        username=self.get_secure_cookie("user"))
        else:
            self.render('modules/widget/tologinfo.html')


class widget_editor(tornado.web.UIModule):
    def render(self, router, uid, userinfo):
        kwd = {'router': router,
               'uid': uid,
               }
        return self.render_string('modules/widget/widget_editor.html',
                                  kwd=kwd,
                                  userinfo=userinfo,
                                  )


class widget_search(tornado.web.UIModule):
    def render(self, ):
        self.mcat = MCategory()
        tag_enum = self.mcat.query_pcat(kind='2')
        return self.render_string('modules/widget/widget_search.html',
                                  cat_enum=tag_enum,
                                  tag_enum = tag_enum)


class star_rating(tornado.web.UIModule):
    def render(self, postinfo, userinfo):
        rating = False
        if userinfo:
            rating = mrating.get_rating(postinfo.uid, userinfo.uid)
        if rating:
            pass
        else:
            rating = postinfo.rating
        return self.render_string('modules/widget/star_rating.html',
                                  unescape=tornado.escape.xhtml_unescape,
                                  postinfo=postinfo,
                                  userinfo=userinfo,
                                  rating=rating,
                                  )

class navigate_panel(tornado.web.UIModule):
    def render(self, userinfo):
        return self.render_string('modules/widget/navigate_panel.html',
                                  unescape=tornado.escape.xhtml_unescape,
                                  userinfo=userinfo,
                                  )

class use_f2e(tornado.web.UIModule):
    def render(self, f2ename):
        return self.render_string('modules/usef2e/{0}.html'.format(f2ename),

                                  )