# -*- coding:utf-8 -*-

'''
Testing for map app.
'''
import sys

sys.path.append('')
import time
from datetime import datetime

import peewee
import tornado.escape

from torcms.core import tools
from torcms.model.category_model import MCategory
from torcms.model.label_model import MLabel
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost


class Test_App:
    '''
    Testing for map app.
    '''

    def setup_method(self):
        self.title = '哈哈sdfsdf'
        self.uid = 'g' + tools.get_uu4d()
        self.tag_id = '2342'

        self.slug = 'huio'
        print('setup 方法执行于本类中每条用例之前')

    def teardown_method(self):
        print("function teardown")
        tt = MPost.get_by_uid(self.uid)
        if tt:
            MPost.delete(tt.uid)

        tt = MCategory.get_by_uid(self.tag_id)
        if tt:
            MCategory.delete(self.tag_id)
            MPost2Catalog.remove_relation(self.uid, self.tag_id)
        tt = MLabel.get_by_slug(self.slug)
        if tt:
            MLabel.delete(tt.uid)

    def test_case1(self):
        uid = self.uid
        post_data = {
            'title': self.title,
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'extinfo': '',
            'valid': 1,
            'kind': '1',
        }
        extinfo = {}

        MPost.add_or_update_post(uid, post_data, extinfo)
        tt = MPost.get_by_uid(uid)
        assert tt.uid == uid
        assert tt.title == post_data['title']

    def test_insert2(self):
        uid = self.uid
        post_data = {
            'title': '',
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '9',
            'extinfo': '',
        }
        extinfo = {}

        MPost.add_or_update_post(uid, post_data, extinfo)
        tt = MPost.get_by_uid(uid)

        assert tt is None

        # MPost.delete(uid)

    def test_insert3(self):
        uid = self.uid
        post_data = {
            'title': 'title1',
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '9',
            'extinfo': '',
        }
        uu = MPost.add_or_update_post(self.uid, post_data)

        assert uu == uid

    def test_insert5(self):
        uid = self.uid
        post_data = {
            'title': '天天',
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '2',
            'extinfo': '',
        }
        uu = MPost.add_or_update_post(self.uid, post_data)
        assert uu == uid

    def test_insert8(self):
        uid = self.uid
        post_data = {
            'title': self.title,
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '2',
            'extinfo': '',
        }
        uu = MPost.add_or_update_post(self.uid, post_data)
        tt = MPost.get_by_uid(uid)

        assert tt.uid == uu

    def add_message(self, **kwargs):
        post_data = {
            'name': kwargs.get('name', 'category'),
            'slug': kwargs.get('slug', self.slug),
            'order': kwargs.get('order', '0'),
            'kind': kwargs.get('kind1', '1'),
            'pid': kwargs.get('pid', '0000'),
        }
        tf = MCategory.add_or_update(self.tag_id, post_data)
        assert tf == self.tag_id
        p_d = {
            'title': kwargs.get('title', self.title),
            'cnt_md': kwargs.get('cnt_md', 'grgr'),
            'time_create': kwargs.get('time_create', '1992'),
            'time_update': kwargs.get('time_update', '1996070600'),
            'user_name': kwargs.get('user_name', 'yuanyuan'),
            'view_count': kwargs.get('view_count', 1),
            'logo': kwargs.get('logo', 'prprprprpr'),
            'memo': kwargs.get('memo', ''),
            'order': kwargs.get('order', '1'),
            'keywords': kwargs.get('keywords', 'sd,as'),
            'extinfo': kwargs.get('extinfo', {}),
            'kind': kwargs.get('kind', '1'),
            'valid': kwargs.get('valid', 1),
        }

        tt = MPost.add_or_update(self.uid, p_d)
        assert tt == self.uid
        MPost2Catalog.add_record(self.uid, self.tag_id)

    def test_query_random(self):
        # MPost.delete(self.uid)
        kwargs = {
            'limit': 300,
            'kind': '2',
        }
        ff = MPost.query_random(**kwargs)
        f = ff.count()

        gg = {
            'user_name': '7788',
            'kind': '2',
        }
        self.add_message(**gg)

        pp = MPost.query_random(**kwargs)
        TF = False
        for i in range(pp.count()):
            if pp[i].uid == self.uid:
                assert pp[i].user_name == '7788'
                TF = True

            else:
                continue
        assert TF == True
        assert pp.count() == f + 1
        # self.teardown_class()

    def test_query_recent(self):
        kwargs = {
            'user_name': '7788',
            'kind': '2',
        }
        self.add_message(**kwargs)

        kwargs = {
            'order_by_create': True,
            'kind': '2',
        }
        pp = MPost.query_recent(num=300, **kwargs)
        TF = False
        for i in range(pp.count()):
            if pp[i].uid == self.uid:
                assert pp[i].user_name == '7788'
                TF = True

            else:
                continue
        assert TF == True
        # self.teardown_class()

    def test_query_all(self):
        kwargs = {
            'user_name': '7788',
            'kind': '2',
        }
        self.add_message(**kwargs)

        kwargs = {'order_by_create': True, 'kind': '2', 'limit': 100}
        pp = MPost.query_all(**kwargs)
        TF = False
        for i in range(pp.count()):
            if pp[i].uid == self.uid:
                assert pp[i].user_name == '7788'
                TF = True

            else:
                continue
        assert TF == True
        # self.teardown_class()

    def test_query_keywords_empty(self):
        kwargs = {
            'keywords': '',
            'user_name': '7788',
            'kind': '1',
        }
        self.add_message(**kwargs)

        pp = MPost.query_keywords_empty()
        TF = False
        for i in range(pp.count()):
            if pp[i].uid == self.uid:
                assert pp[i].user_name == '7788'
                TF = True

            else:
                continue
        assert TF == True
        # self.teardown_class()

    def test_query_recent_edited(self):
        kwargs = {
            'keywords': '',
            'user_name': '7788',
            'kind': '1',
        }
        self.add_message(**kwargs)

        pp = MPost.query_recent_edited(1539069122)
        TF = False
        for i in range(pp.count()):
            if pp[i].uid == self.uid:
                assert pp[i].user_name == '7788'
                TF = True

            else:
                continue
        assert TF == True
        # self.teardown_class()

    def test_query_dated(self):
        pp = MPost.query_dated()

        # ToDo: the count ?

        assert pp.count() >= 0
        # self.teardown_class()

    def test_query_cat_recent(self):
        kwargs = {
            'keywords': '',
            'user_name': '7788',
            'kind': '1',
            'extinfo': 'def_tag_arr',
        }
        self.add_message(**kwargs)
        pp = MPost.query_cat_recent(self.tag_id, num=100)
        TF = False
        for i in range(pp.count()):
            if pp[i].uid == self.uid:
                assert pp[i].user_name == '7788'
                TF = True
            else:
                continue
        assert TF == True
        # self.teardown_class()

    def test_query_most_pic(self):
        kwargs = {
            'user_name': '7788',
            'kind': '1',
        }
        self.add_message(**kwargs)

        pp = MPost.query_most_pic(300)
        TF = False
        for i in range(pp.count()):
            if pp[i].uid == self.uid:
                assert pp[i].user_name == '7788'
                TF = True

            else:
                continue
        assert TF == True

        # self.teardown_class()

    def test_get_all(self):
        kwargs = {
            'user_name': '7788',
            'kind': '2',
        }
        self.add_message(**kwargs)

        pp = MPost.get_all()
        TF = False
        for i in range(pp.count()):
            if pp[i].uid == self.uid:
                assert pp[i].user_name == '7788'
                TF = True
            else:
                continue
        assert TF == True
        # self.teardown_class()

    # def test_modify_init(self):
    #     kwargs = {
    #
    #         'user_name': '7788',
    #         'keywords': 'kllll',
    #         'kind': '2',
    #
    #     }
    #     self.add_message(**kwargs)
    #
    #     uid = self.uid
    #     post_data = {
    #         'keywords': 'oor',
    #         'kind': '3',
    #     }
    #
    #     MPost.modify_init(uid, post_data)
    #     pp = MPost.get_by_uid(uid)
    #     assert post_data['keywords'] == pp.keywords
    #     assert post_data['kind'] == pp.kind
    #     self.teardown_class()

    # def test_get_view_count(self):
    #     kwargs = {
    #
    #         'user_name': '7788',
    #         'keywords': 'kllll',
    #         'kind': '2',
    #
    #     }
    #     self.add_message(**kwargs)
    #
    #     pp = MPost.get_view_count(self.uid)
    #     assert pp == 1
    #     self.teardown_class()
