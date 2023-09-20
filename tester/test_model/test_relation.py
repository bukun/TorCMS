# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.category_model import MCategory
from torcms.model.label_model import MLabel, MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
from torcms.model.relation_model import MRelation


class TestMRelation():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')

        self.uid = 'r1234'
        self.uid2 = 'r1235'
        self.tag_id = '0111'

    def test_get_app_relations(self, **kwargs):
        # 添加post
        post_data = {
            'title': 'test1',
            'cnt_md': '## test',
            'user_name': 'test',
            'view_count': 1,
            'logo': ' ',
            'keywords': 'test',
            'kind': '1'
        }

        uu1 = MPost.add_or_update(self.uid, post_data)
        assert uu1 == self.uid
        post_data2 = {
            'title': 'test2',
            'cnt_md': '## test2',
            'user_name': 'test2',
            'view_count': 1,
            'logo': ' ',
            'keywords': 'test2',
            'kind': '1'

        }

        uu2 = MPost.add_or_update(self.uid2, post_data2)
        assert uu2 == self.uid2
        # 添加category
        cat_data = {
            'name': kwargs.get('name', 'category'),
            'slug': kwargs.get('slug', 'slug1'),
            'order': kwargs.get('order', '0'),
            'kind': kwargs.get('kind1', '1'),
            'pid': kwargs.get('pid', '0000'),
        }

        cat_id = MCategory.add_or_update(self.tag_id, cat_data)
        assert cat_id == self.tag_id
        MPost2Catalog.add_record(uu1, self.tag_id)

        rel_uid = MRelation.add_relation(uu1, uu2)
        assert rel_uid
        rel_rec = MRelation.get_app_relations(uu2)
        assert rel_rec.count() >= 1
        # assert rel_rec.get().post_id == self.uid

    def teardown_method(self):
        print("function teardown")
        MRelation.delete(self.uid)
        MCategory.delete(self.tag_id)
        MPost.delete(self.uid)
        MPost.delete(self.uid2)
