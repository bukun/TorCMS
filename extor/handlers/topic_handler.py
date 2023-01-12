# -*- coding:utf-8 -*-

'''

'''

import tornado.web
from torcms.handlers.post_handler import PostHandler, update_category, update_label
from torcms.model.post_model import MPost
from torcms.model.category_model import MCategory
from config import router_post


class TopicHandler(PostHandler):
    def initialize(self, **kwargs):
        super(TopicHandler, self).initialize()
        self.kind = kwargs.get('kind', 'q')

    @tornado.web.authenticated
    def _to_add(self, **kwargs):
        '''
        Used for info1.
        '''

        if 'catid' in kwargs:
            catid = kwargs['catid']
            return self._to_add_with_category(catid)

        else:
            if 'uid' in kwargs and MPost.get_by_uid(kwargs['uid']):
                # todo:
                # self.redirect('/{0}/edit/{1}'.format(self.app_url_name, uid))
                uid = kwargs['uid']
            else:
                uid = ''
            self.render('post_{0}/post_add.html'.format(self.kind),
                        tag_infos=MCategory.query_all(by_order=True, kind=self.kind),
                        userinfo=self.userinfo,
                        kwd={
                            'uid': uid,

                        })

    @tornado.web.authenticated
    # @tornado.web.asynchronous
    @tornado.gen.coroutine
    def add(self, **kwargs):
        '''
        in infor.
        '''
        if 'uid' in kwargs:
            uid = kwargs['uid']
        else:
            uid = self._gen_uid()

        post_data, ext_dic = self.__parse_post_data()

        title = post_data['title'].strip()

        if len(title) < 2:
            kwd = {
                'info': 'Title cannot be less than 2 characters',
                'link': '/'
            }
            self.render('misc/html/404.html', userinfo=self.userinfo, kwd=kwd)

        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = 1

        # 在应用中，会有分类的逻辑，需要处理
        if 'gcat0' in post_data:
            pass
        else:
            return False
        ext_dic['def_uid'] = uid  # 此 key 用于更新文档时在历史记录中跟踪原 uid .
        ext_dic['gcat0'] = post_data['gcat0']
        ext_dic['def_cat_uid'] = post_data['gcat0']

        # MPost中并没有分类的逻辑关系
        MPost.add_or_update_post(uid, post_data, extinfo=ext_dic)
        # kwargs.pop('uid', None)  # delete `uid` if exists in kwargs

        self._add_download_entity(ext_dic)

        update_category(uid, post_data)
        update_label(uid, post_data)
        # self.update_label(uid)

        # cele_gen_whoosh.delay()
        tornado.ioloop.IOLoop.instance().add_callback(self.cele_gen_whoosh)
        self.redirect('/{0}/{1}'.format(router_post[self.kind], uid))

    def __parse_post_data(self):
        '''
        fetch post accessed data. post_data, and ext_dic.
        '''
        post_data = {}
        ext_dic = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_') or key.startswith('_tag_'):
                ext_dic[key] = self.get_argument(key, default='')
            else:
                post_data[key] = self.get_arguments(key)[0]

        post_data['user_name'] = self.userinfo.user_name
        post_data['kind'] = self.kind

        # append external infor.

        if 'tags' in post_data:
            ext_dic['def_tag_arr'] = [
                x.strip()
                for x in post_data['tags'].strip().strip(',').split(',')
            ]
        ext_dic = dict(ext_dic, **self.ext_post_data(postdata=post_data))

        return (post_data, ext_dic)
