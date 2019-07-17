# -*- coding:utf-8 -*-
from torcms.model.post2catalog_model import MPost2Catalog

from torcms.core import tools


class TestMPost2Catalog():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = tools.get_uuid()
        self.post_id = '11111'
        self.tag_id = '1111'

    def test_add_record(self):
        MPost2Catalog.add_record(self.post_id, self.tag_id)
        assert True

    def test_just_query_all(self):
        MPost2Catalog.just_query_all()
        assert True

    def test_query_all(self):
        MPost2Catalog.query_all()
        assert True

    def test_remove_relation(self):
        MPost2Catalog.remove_relation(self.post_id, self.tag_id)
        assert True

    def test_remove_tag(self):
        MPost2Catalog.remove_tag(self.tag_id)
        assert True

    def test_query_by_catid(self):
        MPost2Catalog.query_by_catid(self.tag_id)
        assert True

    def test_query_postinfo_by_cat(self):
        MPost2Catalog.query_postinfo_by_cat(self.tag_id)
        assert True

    def test_query_by_post(self):
        MPost2Catalog.query_by_post(self.post_id)
        assert True

    def test_query_count(self):
        MPost2Catalog.query_count()
        assert True

    def test_update_field(self):
        MPost2Catalog.update_field(self.uid, post_id=self.post_id)
        assert True

    def test_count_of_certain_category(self):
        MPost2Catalog.count_of_certain_category(self.tag_id)
        assert True

    def test_query_pager_by_slug(self):
        slug = 'aaaa'
        MPost2Catalog.query_pager_by_slug(slug)
        assert True

    def test_query_by_entity_uid(self):
        MPost2Catalog.query_by_entity_uid(self.post_id)
        assert True

    def test_query_by_id(self):
        MPost2Catalog.query_by_id(self.uid)
        assert True

    def test_get_first_category(self):
        MPost2Catalog.get_first_category(self.uid)
        assert True

    def tearDown(self):
        print("function teardown")
        tt = MPost2Catalog.query_by_id(self.uid)
        if tt:
            MPost2Catalog.del_by_uid(self.uid)
