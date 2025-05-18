# -*- coding:utf-8 -*-
import time

import tornado.escape
from faker import Faker

from torcms.core import tools
from torcms.model.category_model import MCategory
from torcms.model.label_model import MLabel, MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost


class TestMPost:
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.mpost = MPost()
        self.m2c = MPost2Catalog()
        self.ml = MLabel()
        self.m2l = MPost2Label()
        self.labeluid = '9999'
        self.raw_count = self.mpost.get_counts()
        self.post_title = 'ccc'
        self.uid = tools.get_uu4d()
        self.post_id = '66565'
        self.tag_id = '2342'
        self.post_id2 = '89898'
        self.slug = 'huio'
        self.fake = Faker(locale="zh_CN")
        self.add_message()

    def teardown_method(self):
        print("function teardown")

        self.mpost.delete(self.uid)
        MCategory.delete(self.tag_id)
        self.mpost.delete(self.post_id2)
        self.mpost.delete(self.post_id)
        MPost2Catalog.remove_relation(self.post_id, self.tag_id)
        tt = MLabel.get_by_slug(self.slug)
        if tt:
            MLabel.delete(tt.uid)

    def test_insert(self):
        raw_count = self.mpost.get_counts()

        post_data = {
            'title': self.post_title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        self.mpost.add_or_update(self.uid, post_data)
        new_count = self.mpost.get_counts()

        tt = self.mpost.get_by_uid(self.uid)
        assert tt.title == post_data['title']
        assert tt.cnt_md == tornado.escape.xhtml_unescape(post_data['cnt_md'])
        assert tt.cnt_html == tools.markdown2html(post_data['cnt_md'])
        assert raw_count + 1 == new_count

    def test_insert_2(self):
        '''Wiki insert: Test invalid title'''

        post_data = {
            'title': '',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        uu = self.mpost.add_or_update(self.uid, post_data)
        assert uu == False

        post_data = {
            'title': '1',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        uu = self.mpost.add_or_update(self.uid, post_data)
        assert uu == False

        post_data = {
            'title': '天',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        uu = self.mpost.add_or_update(self.uid, post_data)

        assert uu == False

    def add_message(self, **kwargs):
        post_data = {
            'name': kwargs.get('name', 'category'),
            'slug': kwargs.get('slug', self.slug),
            'order': kwargs.get('order', '0'),
            'kind': kwargs.get('kind1', '1'),
            'pid': kwargs.get('pid', '0000'),
        }
        MCategory.add_or_update(self.tag_id, post_data)

        p_d = {
            'title': kwargs.get('title', 'iiiii'),
            'cnt_md': kwargs.get('cnt_md', self.fake.text()),
            'time_create': kwargs.get('time_create', '1992'),
            'time_update': kwargs.get('time_update', '1996070600'),
            'user_name': kwargs.get('user_name', 'yuanyuan'),
            'view_count': kwargs.get('view_count', 1),
            'logo': kwargs.get('logo', 'prprprprpr'),
            'memo': kwargs.get('memo', ''),
            'order': kwargs.get('order', '1'),
            'keywords': kwargs.get('keywords', ''),
            'extinfo': kwargs.get('extinfo', {}),
            'kind': kwargs.get('kind2', '1'),
            'valid': kwargs.get('valid', 1),
        }
        post_id = kwargs.get('post_id', self.post_id)

        MPost.add_or_update(post_id, p_d)

        MPost2Catalog.add_record(self.post_id, self.tag_id)

    def test_get_by_title(self):
        post_data = {
            'title': self.post_title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        uid = self.mpost.add_or_update(self.uid, post_data)

        ss = self.mpost.get_by_uid(uid)
        assert ss.title == post_data['title']

    def test_get_by_title2(self):
        '''Test Wiki title with SPACE'''

        post_data = {
            'title': '  ' + self.post_title + '  ',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        uid = self.mpost.add_or_update(self.uid, post_data)

        ss = self.mpost.get_by_uid(uid)
        assert ss.title == self.post_title

    def test_query_cat_random(self):
        p = {'limit': 300}
        TF = False
        qq = self.mpost.query_cat_random(self.tag_id, **p)
        for i in qq:
            if i.uid == self.post_id:
                TF = True

        assert TF

    def test_query_recent_most(self):
        recs = self.mpost.query_recent_most(num=3000)
        is_true = False
        for rec in recs:
            print(rec.uid)
            if rec.uid == self.post_id:
                is_true = True

        assert is_true

    def test_query_recent(self):
        qq = self.mpost.query_recent(num=300)
        TF = False
        for i in qq:
            if i.uid == self.post_id:
                TF = True

        assert TF

    def test_query_all(self):
        kwargs = {
            'limit': 300,
        }
        pp = self.mpost.query_all(**kwargs)
        TF = False
        for i in pp:
            if i.uid == self.post_id:
                TF = True

        assert TF

    def test_query_keywords_empty(self):
        pp = self.mpost.query_keywords_empty()
        TF = False
        for i in pp:
            if i.uid == self.post_id:
                TF = True

        assert TF

    def test_query_dated(self):
        qq = self.mpost.query_dated(num=2000)

        TF = False
        for i in qq:
            if i.uid == self.post_id:
                TF = True

        assert TF

    def test_query_most_pic(self):
        qq = self.mpost.query_most_pic(300)
        TF = False
        for i in qq:
            if i.uid == self.post_id:
                TF = True

        assert TF

    def test_query_cat_recent(self):
        qq = self.mpost.query_cat_recent(self.tag_id, num=300)
        TF = False

        for i in qq:
            if i.uid == self.post_id:
                TF = True

        assert TF

    def test_query_most(self):
        qq = self.mpost.query_most(num=300)
        assert len(qq) <= 300

        # TF = False
        # for i in qq:
        #     if i.uid == self.post_id:
        #         TF = True
        # assert TF

    def test_update_view_count_by_uid(self):
        post_data = {
            'title': self.post_title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        self.mpost.add_or_update(self.uid, post_data)

        rec = self.mpost.get_by_uid(self.uid)

        viewcount0 = rec.view_count
        assert viewcount0 >= 1
        for x in range(100):
            self.mpost.update_misc(rec.uid, count=True)

        viewcount1 = self.mpost.get_by_uid(self.uid).view_count

        assert viewcount1 >= 101

    def test_upate(self):
        y = {'logo': '123123'}
        self.add_message(**y)
        qq = {'title': 'oppssss', 'logo': 'fffff', 'cnt_md': 'iiii', 'user_name': 'yy'}
        self.mpost.add_or_update(self.post_id, qq)
        aa = self.mpost.get_by_uid(self.post_id)
        assert aa.logo == qq['logo']
        assert aa.title == qq['title']

    def test_get_by_uid(self):
        y = {'logo': '123123'}
        self.add_message(**y)
        a = self.mpost.get_by_uid(self.post_id)
        assert a.logo == y['logo']

    def test_get_counts(self):
        a = self.mpost.get_counts()
        self.add_message()
        b = self.mpost.get_counts()
        assert a + 1 >= b

    def test_update_cnt(self):
        self.add_message()
        qq = {'cnt_md': 'iiii', 'user_name': ' yy  '}
        self.mpost.update_cnt(self.post_id, qq)
        bb = self.mpost.get_by_uid(self.post_id)
        assert bb.cnt_md == qq['cnt_md']

    def test_update_order(self):
        self.add_message()

        self.mpost.update_order(self.post_id, '1')
        bb = self.mpost.get_by_uid(self.post_id)
        assert bb.order == '1'

    def test_add_or_update(self):
        bb = self.mpost.get_by_uid(self.post_id)

        assert bb
        p_d = {
            'title': 'iiiii',
            'cnt_md': 'grgr',
            'time_create': '1992',
            'time_update': '1996070600',
            'user_name': 'yuanyuan',
            'view_count': '1',
            'logo': 'prprprprpr',
            'memo': '',
            'order': '1',
            'keywords': '',
            'extinfo': {},
            'kind': '1',
            'valid': '1',
        }
        self.mpost.add_or_update(self.post_id, p_d)
        bb = self.mpost.get_by_uid(self.post_id)
        assert bb.title == p_d['title']
        qq = {'title': 'oppssss', 'logo': 'fffff', 'cnt_md': 'iiii', 'user_name': 'yy'}
        self.mpost.add_or_update(self.post_id, qq)
        aa = self.mpost.get_by_uid(self.post_id)

        assert aa.logo == qq['logo']
        assert aa.title == qq['title']

    def test_query_random(self):
        q = {'num': 3000}
        qq = self.mpost.query_random(**q)

        TF = False
        for i in qq:
            if i.uid == self.post_id:
                TF = True

        assert TF

    def test_query_recent_edited(self):
        qq = self.mpost.query_recent_edited(1555)

        TF = False
        for i in qq:
            if i.uid == self.post_id:
                TF = True

        assert TF

    def test_query_by_tag(self):
        TF = False

        qq = self.mpost.query_by_tag(self.tag_id)
        print(qq.count())

        for i in qq:
            print(i.title)
            if i.uid == self.post_id:
                TF = True

        assert TF

    def test_query_cat_recent_with_label(self):
        name = 'kkkk'
        p_d = {'extinfo': {'def_tag_arr': name}}
        self.add_message(**p_d)

        self.mpost.query_cat_recent_with_label(self.tag_id, label=name, num=300)
        qq = self.mpost.get_by_uid(self.post_id)
        assert qq.extinfo['def_tag_arr'] == p_d['extinfo']['def_tag_arr']

    def test_query_cat_recent_no_label(self):
        qq = self.mpost.query_cat_recent_no_label(self.tag_id, num=300)
        tf = False
        for i in qq:
            if i.uid == self.post_id:
                tf = True
                break

        assert tf

    def test_query_total_cat_recent(self):
        name = 'kkkk'
        p_d = {'extinfo': {'def_tag_arr': name}}
        self.add_message(**p_d)
        qq = self.mpost.query_total_cat_recent(
            [self.tag_id, '9090'], label=name, num=300
        )
        tf = False
        for i in qq:
            if i.uid == self.post_id:
                tf = True
                break

        assert tf

    def test_query_total_cat_recent_no_label(self):
        qq = self.mpost.query_total_cat_recent_no_label([self.tag_id], num=300)
        tf = False
        for i in qq:
            if i.uid == self.post_id:
                tf = True
                break

        assert tf

    # def test_get_next_record(self):
    #     p = {
    #         'time_create': tools.timestamp()
    #     }
    #     self.add_message(**p)
    #     time.sleep(5)
    #     q = {
    #         'post_id': self.post_id2,
    #         'title': '90909090',
    #         'cnt_md': 'oosdfsfofsf',
    #         'time_create': tools.timestamp()
    #     }
    #     self.add_message(**q)
    #     qq = self.mpost.get_next_record(self.post_id2)
    #     assert qq.uid == self.post_id
    #
    # def test_get_previous_record(self):
    #     p = {
    #         'time_create': tools.timestamp(),
    #         'post_id': self.post_id
    #     }
    #     self.add_message(**p)
    #     time.sleep(5)
    #     q = {
    #         'post_id': self.post_id2,
    #         'title': '90909090',
    #         'cnt_md': 'oosdfsfofsf',
    #         'time_create': tools.timestamp()
    #     }
    #     self.add_message(**q)
    #     qq = self.mpost.get_previous_record(self.post_id)
    #     assert qq.uid == self.post_id2

    def test_get_all(self):
        eee = self.mpost.get_all(kind='1')
        TF = False
        for i in eee:
            if self.post_id == i.uid:
                TF = True

        assert TF

    def test_update_jsonb(self):
        p = {'ii': 'ii00ii'}

        self.mpost.update_jsonb(self.post_id, p)
        aa = self.mpost.get_by_uid(self.post_id)

        assert aa.extinfo == p

    def test_modify_meta(self):
        p_d = {
            'title': 'qqqii',
            'cnt_md': 'qwqwqw',
            'time_create': '1999',
            'time_update': '2019',
            'user_name': 'max',
            'view_count': '1',
            'logo': 'opps',
            'memo': '',
            'order': '1',
            'extinfo': {},
            'kind': '1',
            'valid': '1',
        }
        self.mpost.add_or_update_post(self.post_id, p_d)
        aa = self.mpost.get_by_uid(self.post_id)

        assert aa.title == p_d['title']

    def test_query_most_by_cat(self):
        a = self.mpost.query_most_by_cat(catid=self.tag_id, kind='1')
        tf = False
        for i in a:
            if i.uid == self.post_id:
                tf = True
                break

        assert tf

    def test_query_least_by_cat(self):
        a = self.mpost.query_least_by_cat(cat_str=self.tag_id, kind='1')
        tf = False
        for i in a:
            if i.uid == self.post_id:
                tf = True
                break

        assert tf

    def test_get_by_keyword(self):
        p_d = {'title': 'yyyyy'}
        self.add_message(**p_d)
        aa = self.mpost.get_by_keyword('yy', kind='1')
        tf = False
        for i in aa:
            if i.uid == self.post_id:
                tf = True
                break

        assert tf

    def test_query_extinfo_by_cat(self):
        oo = 'd99s9s'
        p_d = {'extinfo': {'def_cat_uid': oo}}
        self.add_message(**p_d)
        aa = self.mpost.query_extinfo_by_cat(oo, kind='1')
        tf = False
        for i in aa:
            if i.uid == self.post_id:
                tf = True
                break

        assert tf

    def test_query_by_tagname(self):
        oo = 'd99s9s'
        p_d = {'extinfo': {'def_tag_arr': oo}}
        self.add_message(**p_d)
        aa = self.mpost.query_by_tagname(oo, kind='1')
        tf = False
        for i in aa:
            if i.uid == self.post_id:
                tf = True
                break

        assert tf

    def test_query_pager_by_tag(self):
        oo = 'd99s9s'
        p_d = {'extinfo': {'def_tag_arr': oo}}
        self.add_message(**p_d)
        aa = self.mpost.query_pager_by_tag(oo, kind='1')
        tf = False
        for i in aa:
            if i.uid == self.post_id:
                tf = True
                break

        assert tf

    def test_add_meta(self):
        p_d = {
            'title': 'qqqii',
            'cnt_md': 'qwqwqw',
            'time_create': '1999',
            'time_update': '2019',
            'user_name': 'max',
            'view_count': '1',
            'logo': 'opps',
            'memo': '',
            'order': '1',
            'kind': '1',
            'valid': 1,
        }
        self.mpost.add_or_update_post(self.post_id, p_d)

        aa = self.mpost.get_by_uid(self.post_id)

        assert aa.title == p_d['title']

    def test_query_under_condition(self):
        oo = {'def_tag_arr': 'd99s9s'}
        p_d = {'extinfo': oo}
        self.add_message(**p_d)
        qq = self.mpost.query_under_condition(oo, kind='1')
        tf = False
        for i in qq:
            if i.uid == self.post_id:
                tf = True
                break

        assert tf

    def test_query_list_pager(self):
        oo = {'def_tag_arr': 'd99s9s'}
        p_d = {'extinfo': oo}
        self.add_message(**p_d)
        qq = self.mpost.query_list_pager(oo, 1, kind='1')
        tf = False
        for i in qq:
            if i.uid == self.post_id:
                tf = True
                break

        assert tf

    def test_count_of_certain_kind(self):
        a = self.mpost.count_of_certain_kind(1)

        assert a >= 1

    def test_total_number(self):
        a = self.mpost.total_number(1)

        assert a >= 1
