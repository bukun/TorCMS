# -*- coding:utf-8 -*-


import tornado.escape
import tornado.web
import tornado.gen

import json
from torcms.model.infor2label_model import MInfor2Label
from torcms.model.info_model import MInfor
from torcms.model.info_relation_model import MInforRel
from torcms.model.evaluation_model import MEvaluation
from torcms.model.usage_model import MUsage
from torcms.model.infor2catalog_model import MInfor2Catalog
from torcms.model.reply_model import MReply
from torcms.handlers.post_handler import PostHandler
from torcms.model.info_hist_model import MInfoHist
from config import router_post
from torcms.core.tools import logger


class AdminPostHandler(PostHandler):
    def initialize(self, hinfo=''):
        super(AdminPostHandler, self).initialize()
        self.mevaluation = MEvaluation()
        self.mpost2label = MInfor2Label()
        self.mpost2catalog = MInfor2Catalog()
        self.mpost = MInfor()
        self.musage = MUsage()

        self.mrel = MInforRel()
        self.mreply = MReply()
        self.mpost_hist = MInfoHist()

    def get(self, url_str=''):
        if self.userinfo and self.userinfo.role[2] >= '3':
            pass
        else:
            return False
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 2:
            if url_arr[0] in ['_edit']:
                self.to_edit(url_arr[1])
        else:
            return False

    def post(self, url_str=''):
        if self.userinfo and self.userinfo.role[2] >= '3':
            pass
        else:
            return False

        url_arr = self.parse_url(url_str)

        if len(url_arr) == 2:
            if url_arr[0] in ['_edit']:
                self.update(url_arr[1])
        else:
            return False

    @tornado.web.authenticated
    def to_edit(self, post_uid):
        postinfo = self.mpost.get_by_uid(post_uid, )
        json_cnt = json.dumps(postinfo.extinfo, indent=True)
        self.render('man_post/admin_post.html',
                    postinfo=postinfo,
                    sig_dic=router_post,
                    userinfo=self.userinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    json_cnt=json_cnt,
                    )

    @tornado.web.authenticated
    def update(self, post_uid):
        post_data = self.get_post_data()

        logger.info('admin post update: {0}'.format(post_data))

        ext_dic = {}
        ext_dic['def_uid'] = post_uid
        ext_dic['def_cat_uid'] = post_data['gcat0']
        ext_dic['def_cat_pid'] = self.mcat.get_by_uid(post_data['gcat0']).pid

        self.mpost.update_kind(post_uid, post_data['kcat'])
        self.mpost.update_jsonb(post_uid, ext_dic)
        self.update_category(post_uid)

        self.redirect('/{0}/{1}'.format(router_post[post_data['kcat']], post_uid))
