# -*- coding:utf-8 -*-
from torcms.model.catalog_model import MCatalog
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost


class TestMCatalog():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.post_id = 'r42w2'
        self.slug = 'huohuohuo'
        self.tag_id = 'xx00'

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
            'valid': kwargs.get('valid', 0),

        }
        post_id = kwargs.get('post_id', self.post_id)

        MPost.create_post(post_id, p_d)

        MPost2Catalog.add_record(self.post_id, self.tag_id)

    def test_query_by_slug(self):
        self.add_message()
        aa = MCatalog.query_by_slug(self.slug)
        tf = False
        for i in aa:
            if i.uid == self.post_id:
                tf = True
        assert tf
        self.tearDown()

    def test_query_all(self):
        self.add_message()
        aa = MCatalog.query_all()
        tf = False
        for i in aa:
            if i.slug == self.slug:
                tf = True
        assert tf
        self.tearDown()

    def tearDown(self):
        print("function teardown")
        MPost.delete(self.post_id)
        MCategory.delete(self.tag_id)
        MPost2Catalog.remove_relation(self.post_id, self.tag_id)
        self.uid = ''
