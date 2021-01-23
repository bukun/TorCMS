# -*- coding:utf-8 -*-

# 统计访问来源

import datetime
from concurrent.futures import ThreadPoolExecutor

from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.core.tools import logger
from torcms.model.referrer_model import MReferrer


class Referrer(BaseHandler):
    '''
    The basic HTML Page handler.
    '''
    executor = ThreadPoolExecutor(2)

    def initialize(self, **kwargs):
        super().initialize()
        self.kind = kwargs.get('kind', 'r')

    def get(self, *args, **kwargs):
        url_str = args[0]

        if url_str == '' or url_str == 'index':
            self.index()
        else:
            self.show404()

    def post(self, *args, **kwargs):

        url_str = args[0]
        logger.info('Post url: {0}'.format(url_str))
        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['_add']:
            print("*" * 50)
            print(len(url_arr))

            self.add()
        else:
            self.show404()

    def index(self):
        '''
        The default page of POST.
        '''
        postinfo = MReferrer.query_all()
        self.render('post_{0}/post_index.html'.format(self.kind),
                    userinfo=self.userinfo,
                    postinfo=postinfo,
                    kwd={
                        'uid': '',
                    })

    def _gen_uid(self):
        '''
        Generate the ID for post.
        :return: the new ID.
        '''
        cur_uid = self.kind + tools.get_uu4d()
        while MReferrer.get_by_uid(cur_uid):
            cur_uid = self.kind + tools.get_uu4d()
        return cur_uid

    def fetch_post_data(self):
        '''
        fetch post accessed data. post_data, and ext_dic.
        '''
        post_data = {}
        ext_dic = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_'):
                ext_dic[key] = self.get_argument(key, default='')
            else:
                post_data[key] = self.get_arguments(key)[0]

        post_data['kind'] = self.kind

        # append external infor.

        if 'tags' in post_data:
            ext_dic['def_tag_arr'] = [
                x.strip()
                for x in post_data['tags'].strip().strip(',').split(',')
            ]
        ext_dic = dict(ext_dic, **self.ext_post_data(postdata=post_data))

        return (post_data, ext_dic)

    def add(self, **kwargs):
        '''
        in infor.
        '''

        if 'uid' in kwargs:
            uid = kwargs['uid']
        else:
            uid = self._gen_uid()
        post_data, ext_dic = self.fetch_post_data()
        postinfo = MReferrer.get_by_userip(post_data['userip'])
        if postinfo:
            for x in postinfo:
                olddate = datetime.datetime.fromtimestamp(x.time_create)
                oldid = x.uid
            newdate = datetime.datetime.now()
            difference = (newdate - olddate).days
            if difference <= 6:
                print('此用户已经存入数据库内')
            else:
                MReferrer.modify_meta(oldid, post_data)
        else:
            MReferrer.add_meta(uid, post_data)

    def ext_post_data(self, **kwargs):
        '''
        The additional information.  for add(), or update().
        '''
        _ = kwargs
        return {}
