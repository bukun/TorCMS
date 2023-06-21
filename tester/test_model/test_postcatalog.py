# -*- coding:utf-8 -*-
from torcms.core import tools
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost


class TestMCategory():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = 'hy00'
        self.slug = 'sluug'

        self.postid = 'greww'
        self.add_message()

    def test_add_or_update(self):
        post_data = {
            'name': 'category',
            'slug': self.slug,
            'order': '1',
            'kind': '1',
            'pid': 'z100',
        }
        MCategory.add_or_update(self.uid, post_data)
        a = MCategory.get_by_uid(self.uid)
        assert a.pid == post_data['pid']

        post_data2 = {
            'name': 'adsfdsf',
            'pid': 'z222',
            'slug': 'ssskug',

        }
        MCategory.add_or_update(self.uid, post_data2)
        a2 = MCategory.get_by_uid(self.uid)

        assert a2.name == post_data2['name']

    def add_message(self, **kwargs):
        post_data = {
            'name': kwargs.get('name', 'category'),
            'slug': kwargs.get('slug', self.slug),
            'order': kwargs.get('order', '0'),
            'kind': kwargs.get('kind', '1'),
            'pid': kwargs.get('pid', '0000'),
        }
        MCategory.add_or_update(self.uid, post_data)

        p_d = {
            'title': 'iiiii',
            'cnt_md': 'grgr',
            'time_create': '1992',
            'time_update': '1996',
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

        MPost.add_or_update(self.postid, p_d)
        MPost2Catalog.add_record(self.postid, self.uid)

    def test_update(self):
        post_data = {
            'name': 'adsfdsf',
            'pid': 'z222',
        }

        MCategory.update(self.uid, post_data)
        a = MCategory.get_by_uid(self.uid)

        assert a.name == post_data['name']

    def test_update_count(self):

        MCategory.update_count(self.uid)

        a = MCategory.get_by_uid(self.uid)

        assert a.count >= 0

    def test_get_by_slug(self):

        a = MCategory.get_by_slug(self.slug)

        assert a

    def test_query_field_count(self):

        a = MCategory.query_field_count(500)

        TF = False
        for i in range(a.count()):
            if a[i].uid == self.uid:
                TF = True

        assert TF

    def test_get_qian2(self):
        post_data = {
            'pid': '1992'
        }
        self.add_message(**post_data)
        a = MCategory.get_qian2(self.uid[:2])
        TF = False
        for i in range(a.count()):
            if a[i].pid == post_data['pid']:
                TF = True

        assert TF

    def test_get_by_uid(self):
        post_data = {
            'pid': '1992'
        }
        self.add_message(**post_data)
        a = MCategory.get_by_uid(self.uid)
        TF = False
        if a.pid == post_data['pid']:
            TF = True

        assert TF

    def test_query_all(self):

        a = MCategory.query_all()

        TF = False
        for i in range(a.count()):
            if a[i].uid == self.uid:
                TF = True

        assert TF

    def test_query_uid_starts_with(self):

        a = MCategory.query_uid_starts_with(self.uid[:2])
        TF = False
        for i in range(a.count()):
            if a[i].uid == self.uid:
                TF = True

        assert TF

    def test_query_pcat(self):

        a = MCategory.query_pcat()
        TF = False
        for i in range(a.count()):
            if a[i].uid == self.uid:
                TF = True

        assert TF

    def test_query_sub_cat(self):

        a = MCategory.query_sub_cat('0000')
        TF = False

        for i in range(a.count()):
            if a[i].uid == self.uid:
                TF = True

        assert TF



    def test_query_kind_cat(self):

        a = MCategory.query_kind_cat('1')
        TF = False
        for i in range(a.count()):
            if a[i].uid == self.uid:
                TF = True

        assert TF

    def test_get_parent_list(self):

        recs = MCategory.get_parent_list()
        TF = False
        for i in recs:
            if i.uid == self.uid:
                TF = True

        assert TF

    def teardown_method(self):
        print("function teardown")


        MPost.delete(self.postid)

        MPost2Catalog.remove_relation(self.postid, self.uid)
        MCategory.delete(self.uid)