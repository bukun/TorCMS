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

    def test_query_random(self):

        kwargs = {
            'limit': 3,
            'kind': '0',
        }

        pp = MPost.query_random(**kwargs)
        print('8' * 100)
        # print(pp)
        # print(pp.count())
        # print(pp)
        # print(pp[0].title)
        # print(pp.title)
        assert pp.count()==0

        post_data = {
            'title': self.title,
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '0',
            'extinfo': ''
        }
        MPost.add_meta(self.uid, post_data)



        pp=MPost.query_random(**kwargs)
        print('8'*100)
        # print(pp)
        # print(pp.count())
        # print(pp)
        # print(pp[0].title)
        # print(pp.title)
        assert pp.count() <= 3
        assert pp[0].title==self.title




    def test_query_recent(self):
        kwargs = {
            'kind': '0',
            'order_by_create':True,
        }

        pp=MPost.query_recent(**kwargs)
        # print('00000000000000000000000')
        # print(pp.count())
        assert pp.count()==0



        post_data = {
            'title': self.title,
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '0',
            'extinfo': ''
        }
        MPost.add_meta(self.uid, post_data)

        MPost.query_recent(**kwargs)
        # print('000000000000000000000999')
        # print(pp[0].logo)
        # print(pp.count())
        assert pp[0].logo=='/static/'


    def test_query_all(self):
        kwargs = {
        }
        pp=MPost.query_all(**kwargs)
        print(pp[1].uid)
        print(pp.count())


        post_data = {
            'title': self.title,
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '0',
            'extinfo': ''
        }
        MPost.add_meta(self.uid, post_data)

        kwargs = {
            'limit': 3,
            'kind': '0',
        }
        pp=MPost.query_all(**kwargs)
        assert pp[0].uid==self.uid

    def test_query_keywords_empty(self):
        pp=MPost.query_keywords_empty()
        d=pp.count()
        print(d)

        post_data = {
            'title': self.title,
            'keywords': '',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '1',
            'extinfo': ''
        }
        MPost.add_meta(self.uid, post_data)
        pp = MPost.query_keywords_empty()

        assert pp.count()==d+1

    def test_query_recent_edited(self):
        pp=MPost.query_recent_edited(1539069122)
        d = pp.count()
        print(d)

        post_data = {
            'title': self.title,
            'keywords': 'lalalala',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '1',
            'extinfo': ''
        }
        MPost.add_meta(self.uid, post_data)
        pp = MPost.query_recent_edited(1539069122)

        print(pp.count())
        assert pp.count()==d+1

    def test_query_dated(self):
        pp=MPost.query_dated()

        assert pp.count()==8

    def test_query_most_pic(self):
        b=MPost.query_most_pic(300)
        print(b.count())


        post_data = {
            'title': 'lililala',
            'keywords': 'hiahia',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '',
            'user_name': 'ss',
            'kind': '1',
            'extinfo': ''
        }
        MPost.add_meta(self.uid, post_data)
        d = MPost.query_most_pic(300)
        print(d.count())
        assert b.count()==d.count()

    def test_get_all(self):
        a=MPost.get_all()
        post_data = {
            'title': self.title,
            'keywords': 'lalalala',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '2',
            'extinfo': ''
        }
        MPost.add_meta(self.uid, post_data)
        b=MPost.get_all()
        assert a.count()==b.count()

    def test_modify_init(self):
        uid=self.uid
        post_data = {
            'kind': '9',
            'keywords': 'k',
        }


        MPost.modify_init(uid, post_data)
        pp=MPost.get_by_uid(uid)
        print('6' * 100)
        print(pp)
        # print(pp.count())
        assert pp==None



        post_data2 = {
            'title': self.title,
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '9',
            'extinfo': ''
        }
        MPost.add_meta(uid, post_data2)


        MPost.modify_init(uid, post_data)
        pp=MPost.get_by_uid(uid)
        print('6' * 100)
        # print(pp.kind)
        # print(pp.count())
        assert pp.kind=='9'
        assert pp.keywords=='k'

    def test_get_view_count(self):
        post_data = {
            'title': self.title,
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '0',
            'extinfo': ''
        }
        MPost.add_meta(self.uid, post_data)
        pp= MPost.get_view_count(self.uid)
        # print(pp)
        # print(pp[0].kind)

        assert pp==0

    def tearDown(self):
        print("function teardown")
        tt = MPost.get_by_uid(self.uid)
        if tt:
            MPost.delete(tt.uid)