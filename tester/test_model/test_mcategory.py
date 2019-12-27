# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.category_model import MCategory
import tornado.escape

from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost


class TestMCategory():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = '9384'
        self.tag_id =self.uid
        self.post_id='02934'
        self.slug = 'ccc'

    def add_message(self, **kwargs):
        post_data = {
            'name': kwargs.get('name', 'category'),
            'slug': kwargs.get('slug', 'slug'),
            'order': kwargs.get('order', '0'),
            'kind': kwargs.get('kind1', '1'),
            'pid': kwargs.get('pid', '0000'),
        }
        MCategory.add_or_update(self.tag_id, post_data)

        p_d = {
            'title': kwargs.get('title', 'iiiii'),
            'cnt_md': kwargs.get('cnt_md', 'grgr'),
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
        MPost.get_by_uid(post_id)

        MPost.create_post(post_id, p_d)

        MPost2Catalog.add_record(self.post_id, self.tag_id)

    def test_add_or_update(self):
        uid = self.uid
        post_data = {
            'name': 'titlesdf',
            'slug': self.slug,
            'order': '1',
            'type': 1,
            'tmpl': 0,
            'pid': '0000',
            'count': 0
        }

        newid = MCategory.add_or_update(uid, post_data)

        tt = MCategory.get_by_slug(self.slug)
        # assert tt == newid


        '''Wiki insert: Test invalid title'''
        post_data = {
            'name': '',
            'slug': 'asvaa',
            'order': '2',
            'type': 1,

            'tmpl': 0,
            'pid': '0000',
        }
        uu = MCategory.add_or_update(self.uid, post_data)
        # assert uu == False

        post_data = {
            'name': 'f',
            'slug': self.uid,
            'order': '3',
            'type': 1,

            'tmpl': 0,
            'pid': '0000',
        }
        uu = MCategory.add_or_update(self.uid, post_data)
        # assert uu == False

    def test_update(self):
        # MCategory.update('0000')
        assert True

    def test_update_count(self):
        MCategory.update_count('0000')
        assert True

    def test_get_by_slug(self):
        MCategory.get_by_slug(self.slug)
        assert True

    def test_query_field_count(self):
        MCategory.query_field_count(8)
        assert True

    def test_query_all(self):
        MCategory.query_all()
        assert True

    def test_query_uid_starts_with(self):
        MCategory.query_uid_starts_with('01')
        assert True

    def test_query_pcat(self):
        MCategory.query_pcat()
        assert True

    def test_query_sub_cat(self):
        MCategory.query_sub_cat('0100')
        assert True

    def test_query_kind_cat(self):
        MCategory.query_kind_cat('9')
        assert True

    def test_get_parent_list(self):
        MCategory.get_parent_list()
        assert True

    def test_get_qian2(self):
        MCategory.get_qian2('01')
        assert True

    def test_get_by_uid(self):
        MCategory.get_by_uid(self.uid)
        assert True

    def test_delete(self):
        MCategory.delete(self.uid)
        assert True

    def tearDown(self):
        print("function teardown")
        tt = MPost.get_by_uid(self.uid)

        if tt:
            print('翻翻翻翻翻翻翻翻翻翻翻翻翻翻翻翻翻翻3')
            MPost.delete(self.uid)
        tt = MPost.get_by_uid(self.post_id)
        if tt:
            MCategory.delete(self.tag_id)

            MPost.delete(self.post_id)

            MPost2Catalog.remove_relation(self.post_id, self.tag_id)
            print('545456365635653')
