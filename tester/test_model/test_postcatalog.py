# -*- coding:utf-8 -*-
from torcms.model.category_model import MCategory
from torcms.core import tools


class TestMCategory():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = '0111'
        self.slug = 'slug'

    def test_add_or_update(self):
        post_data = {
            'name': 'category',
            'slug': self.slug,
            'order': '1',
            'kind': '1',
            'pid': 'z100',
        }
        MCategory.add_or_update(self.uid, post_data)
        assert True

    # def test_update(self):
    #     post_data = {
    #         'name': 'adsfdsf',
    #         'slug': self.slug,
    #         'order': '1',
    #         'kind': '1',
    #         'pid': 'z100',
    #     }
    #     MCategory.update(self.uid, post_data)
    #     assert True

    def test_update_count(self):
        MCategory.update_count(self.uid)
        assert True

    def test_get_by_slug(self):
        MCategory.get_by_slug(self.slug)
        assert True

    def test_query_field_count(self):
        MCategory.query_field_count(10)
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
        MCategory.query_sub_cat(self.uid)
        assert True

    def test_query_kind_cat(self):
        MCategory.query_kind_cat('1')
        assert True

    def test_get_parent_list(self):
        MCategory.get_parent_list()
        assert True

    def tearDown(self):
        print("function teardown")
        tt = MCategory.get_by_uid(self.uid)
        if tt:
            MCategory.delete(self.uid)
