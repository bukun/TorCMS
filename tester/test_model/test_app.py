# -*- coding:utf-8 -*-

'''
Testing for map app.
'''

from torcms.core import tools
from torcms.model.post_model import MPost

import time
from datetime import datetime
import peewee
import tornado.escape


class TestApp():
    '''
    Testing for map app.
    '''

    def setup(self):
        print('setup 方法执行于本类中每条用例之前')

        self.title = '哈哈sdfsdf'
        self.uid = 'g' + tools.get_uu4d()

    def test_insert(self):
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

        MPost.add_meta(uid, post_data, extinfo)
        tt = MPost.get_by_uid(uid)
        assert tt.uid == uid

    def test_insert2(self):
        uid = self.uid
        post_data = {

            'title': '',
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '9',
            'extinfo': ''
        }
        extinfo = {}

        MPost.add_meta(uid, post_data, extinfo)
        tt = MPost.get_by_uid(uid)
        assert tt == None

        post_data = {
            'title': '1',
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '9',
            'extinfo': ''
        }
        uu = MPost.add_meta(self.uid, post_data)
        assert uu == False

        post_data = {
            'title': '天',
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '2',
            'extinfo': ''
        }
        uu = MPost.add_meta(self.uid, post_data)
        assert uu == False

        post_data = {
            'title': self.title,
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '2',
            'extinfo': ''
        }
        uu = MPost.add_meta(self.uid, post_data)
        tt = MPost.get_by_uid(uid)
        print(tt)
        assert tt.uid == uu

    def add_message(self, **kwargs):
        '''
        添加测试信息
        '''
        post_data = {
            'title': kwargs.get('title', self.title),
            'keywords': kwargs.get('keywords', 'sd,as'),
            'cnt_md': kwargs.get('cnt_md', '## adslkfjasdf\n lasdfkjsadf'),
            'logo': kwargs.get('logo', '/static/'),
            'user_name': kwargs.get('user_name', 'ss'),
            'kind': kwargs.get('kind', '0'),
            'extinfo': kwargs.get('extinfo', ''),

        }
        MPost.add_meta(self.uid, post_data)

    def test_query_random(self):

        kwargs = {

            'user_name': '7788',
            'kind': '2',

        }
        self.add_message(**kwargs)

        kwargs = {
            'limit': 300,
            'kind': '2',
        }
        pp = MPost.query_random(**kwargs)
        TF = False
        for i in range(pp.count()):
            if pp[i].title == self.title:
                assert pp[i].user_name == '7788'
                TF = True

            else:
                continue
        assert TF == True
        # print('8' * 100)
        # print(pp.count())
        # assert pp==1

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
        pp = MPost.query_recent(**kwargs)
        TF = False
        for i in range(pp.count()):
            if pp[i].title == self.title:
                assert pp[i].user_name == '7788'
                TF = True

            else:
                continue
        assert TF == True

    def test_query_all(self):

        kwargs = {

            'user_name': '7788',
            'kind': '2',

        }
        self.add_message(**kwargs)

        kwargs = {
            'order_by_create': True,
            'kind': '2',
        }
        pp = MPost.query_all(**kwargs)
        TF = False
        for i in range(pp.count()):
            if pp[i].title == self.title:
                assert pp[i].user_name == '7788'
                TF = True

            else:
                continue
        assert TF == True

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
            if pp[i].title == self.title:
                assert pp[i].user_name == '7788'
                TF = True
                print('000')

            else:
                continue
        assert TF == True

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
            if pp[i].title == self.title:
                assert pp[i].user_name == '7788'
                TF = True
                print('000')

            else:
                continue
        assert TF == True

    def test_query_dated(self):
        pp = MPost.query_dated()

        # ToDo: the count ? 

        assert pp.count() >= 0 

    # def test_query_cat_recent(self):
    #     kwargs = {
    #         'keywords': '',
    #         'user_name': '7788',
    #         'kind': '1',
    #         'extinfo':'def_tag_arr'
    #
    #     }
    #     self.add_message(**kwargs)
    #     pp=MPost.query_cat_recent(self.uid)
    #     TF = False
    #     for i in range(pp.count()):
    #         if pp[i].title == self.title:
    #             assert pp[i].user_name == '7788'
    #             TF = True
    #             print('000')
    #
    #         else:
    #             continue
    #     assert TF == True


    def test_query_most_pic(self):

        kwargs = {

            'user_name': '7788',
            'kind': '1',

        }
        self.add_message(**kwargs)

        pp = MPost.query_most_pic(300)
        TF = False
        for i in range(pp.count()):
            if pp[i].title == self.title:
                assert pp[i].user_name == '7788'
                TF = True
                print('000')

            else:
                continue
        assert TF == True

    def test_get_all(self):

        kwargs = {

            'user_name': '7788',
            'kind': '2',

        }
        self.add_message(**kwargs)

        pp = MPost.get_all()
        TF = False
        for i in range(pp.count()):
            if pp[i].title == self.title:
                assert pp[i].user_name == '7788'
                TF = True
                print('000')

            else:
                continue
        assert TF == True

    def test_modify_init(self):
        kwargs = {

            'user_name': '7788',
            'keywords': 'kllll',
            'kind': '2',

        }
        self.add_message(**kwargs)

        uid = self.uid
        post_data = {
            'keywords': 'oor',
            'kind': '3',
        }

        MPost.modify_init(uid, post_data)
        pp = MPost.get_by_uid(uid)
        print('6' * 100)
        print(post_data['keywords'])
        print(pp.keywords)
        # print(pp.count())
        assert post_data['keywords'] == pp.keywords
        assert post_data['kind'] == pp.kind

    def test_get_view_count(self):
        kwargs = {

            'user_name': '7788',
            'keywords': 'kllll',
            'kind': '2',

        }
        self.add_message(**kwargs)

        pp = MPost.get_view_count(self.uid)
        print(pp)
        # print(pp[0].kind)

        assert pp == 0

    def tearDown(self):
        print("function teardown")
        tt = MPost.get_by_uid(self.uid)
        if tt:
            MPost.delete(tt.uid)
