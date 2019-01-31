# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.category_model import MCategory
import tornado.escape


class TestCatalog():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = tools.get_uu4d()
        self.slug = 'ccc'

    def test_insert(self):
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

    def test_insert_2(self):
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
        tt = MCategory.get_by_slug(self.slug)
        if tt:
            MCategory.delete(tt.uid)
