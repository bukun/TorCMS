# -*- coding:utf-8 -*-

'''
Administrator, to change the category of the post.
'''
import json
import tornado.escape
import tornado.web
import tornado.gen
from torcms.handlers.post_handler import PostHandler
from torcms.model.post_model import MPost
from torcms.core.tools import logger
from config import router_post


class PostCategoryHandler(PostHandler):
    '''
    Administrator, to change the category of the post.
    '''

    def initialize(self):
        super(PostCategoryHandler, self).initialize()

    def get(self, *args):
        url_str = args[0]
        if self.userinfo and self.userinfo.role[1] >= '3':
            pass
        else:
            self.redirect('/')
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 2:
            if url_arr[0] in ['_edit']:
                self.__to_edit(url_arr[1])
        else:
            return False

    def post(self, *args):
        url_str = args[0]
        if self.userinfo and self.userinfo.role[1] >= '3':
            pass
        else:
            self.redirect('/')

        url_arr = self.parse_url(url_str)

        if len(url_arr) == 2:
            if url_arr[0] in ['_edit']:
                self.update(url_arr[1])
        else:
            return False

    @tornado.web.authenticated
    def __to_edit(self, post_uid):
        '''
        Show the page for changing the category.
        :param post_uid:
        :return:
        '''
        postinfo = MPost.get_by_uid(post_uid, )
        json_cnt = json.dumps(postinfo.extinfo, indent=True)
        self.render('man_info/post_category.html',
                    postinfo=postinfo,
                    sig_dic=router_post,
                    userinfo=self.userinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    json_cnt=json_cnt)

    @tornado.web.authenticated
    def update(self, post_uid):
        post_data = self.get_post_data()

        logger.info('admin post update: {0}'.format(post_data))

        MPost.update_kind(post_uid, post_data['kcat'])
        # MPost.update_jsonb(post_uid, ext_dic)
        self.update_category(post_uid)

        self.redirect('/{0}/{1}'.format(router_post[post_data['kcat']], post_uid))
