# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.category_model import MCategory
import tornado.escape

from torcms.model.label_model import MLabel
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost


class TestMCategory():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = '9300'
        self.tag_id = self.uid
        self.post_id = '02934'
        self.slug = 'ccgc'

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
            'order': kwargs.get('order1', '1'),
            'keywords': kwargs.get('keywords', ''),
            'extinfo': kwargs.get('extinfo', {}),
            'kind': kwargs.get('kind2', '1'),
            'valid': kwargs.get('valid', 1),

        }
        post_id = kwargs.get('post_id', self.post_id)

        MPost.create_post(post_id, p_d)
        MPost2Catalog.add_record(self.post_id, self.tag_id)

    def test_add_or_update(self):
        self.tearDown()

        post_data = {
            'name': 'titlesdf',
            'slug': self.slug,
            'order': '1',
            'type': 1,
            'tmpl': 0,
            'pid': '0000',
        }
        self.add_message(**post_data)
        tt = MCategory.get_by_uid(self.uid)
        assert tt.name == post_data['name']
        self.tearDown()

    def test_update(self):
        self.tearDown()
        self.add_message()
        post_data = {
            'name': 'chicken',
            'slug': 'hahaha',
            'pid': '9988',
        }
        MCategory.update(self.uid, post_data)
        tt = MCategory.get_by_uid(self.uid)
        assert tt.name == post_data['name']
        assert tt.slug == post_data['slug']
        assert tt.pid == post_data['pid']
        self.tearDown()

    def test_get_by_slug(self):
        self.tearDown()
        self.add_message()
        aa = MCategory.get_by_slug(self.slug)
        assert aa.uid == self.uid
        self.tearDown()

    def test_query_field_count(self):
        self.tearDown()
        aa = MCategory.query_field_count(500)
        tf = True
        for i in aa:
            if i.uid == self.uid:
                tf = False
                break
        assert tf
        self.add_message()
        aa = MCategory.query_field_count(500)
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True
                break
        self.tearDown()
        assert tf

    def test_query_all(self):
        self.tearDown()
        aa = MCategory.query_all()
        tf = True
        for i in aa:
            if i.uid == self.uid:
                tf = False
                break
        assert tf
        self.add_message()
        aa = MCategory.query_all()
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True
                break
        self.tearDown()
        assert tf

    def test_query_uid_starts_with(self):
        self.tearDown()
        aa = MCategory.query_uid_starts_with(self.uid[0:2])
        tf = True
        for i in aa:
            if i.uid == self.uid:
                tf = False
                break
        assert tf
        self.add_message()
        aa = MCategory.query_uid_starts_with(self.uid[0:2])
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True
                break
        self.tearDown()
        assert tf

    def test_query_pcat(self):
        self.tearDown()
        aa = MCategory.query_pcat()
        tf = True
        for i in aa:
            if i.uid == self.uid:
                tf = False
                break
        assert tf
        self.add_message()
        aa = MCategory.query_pcat()
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True
                break
        self.tearDown()
        assert tf

    def test_query_sub_cat(self):
        self.tearDown()
        post_data = {
            'name': 'chicken',
            'slug': 'hahaha',
            'pid': '9988',
        }
        self.add_message(**post_data)
        tt = MCategory.query_sub_cat(post_data['pid'])
        for i in tt:
            if i.uid == self.uid:
                assert i.name == post_data['name']
                assert i.slug == post_data['slug']
        self.tearDown()

    def test_query_kind_cat(self):
        self.tearDown()
        post_data = {
            'name': 'chicken',
            'slug': 'hahaha',
            'kind1': '4',
        }
        self.add_message(**post_data)
        tt = MCategory.query_kind_cat(post_data['kind1'])
        for i in tt:
            if i.uid == self.uid:
                assert i.name == post_data['name']
                assert i.slug == post_data['slug']
        self.tearDown()

    def test_get_parent_list(self):
        self.tearDown()
        self.add_message()
        tt = MCategory.get_parent_list()
        tf = False
        for i in tt:
            if i.uid == self.uid:
                tf = True
        self.tearDown()
        assert tf

    def test_get_qian2(self):
        self.tearDown()
        aa = MCategory.get_qian2(self.uid[0:2])
        tf = True
        for i in aa:
            if i.uid == self.uid:
                tf = False
                break
        assert tf
        self.add_message()
        aa = MCategory.get_qian2(self.uid[0:2])
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True
                break
        self.tearDown()
        assert tf

    def test_get_by_uid(self):
        self.tearDown()
        aa = MCategory.get_by_uid(self.uid)
        assert aa == None
        self.add_message()
        tt = MCategory.get_by_uid(self.uid)
        assert tt.slug == self.slug
        self.tearDown()

    def test_delete(self):
        aa = MCategory.get_by_uid(self.uid)
        assert aa == None
        self.add_message()
        tt = MCategory.get_by_uid(self.uid)
        assert tt.slug == self.slug
        aa = MCategory.delete(self.uid)
        assert aa
        aa = MCategory.get_by_uid(self.uid)
        assert aa == None
        self.tearDown()

    def tearDown(self):
        print("function teardown")
        tt = MPost.get_by_uid(self.uid)

        if tt:
            MPost.delete(self.uid)
        tt = MPost.get_by_uid(self.post_id)
        if tt:
            MCategory.delete(self.tag_id)
            MPost.delete(self.post_id)
            MPost2Catalog.remove_relation(self.post_id, self.tag_id)
        tt = MLabel.get_by_slug(self.slug)
        if tt:
            MLabel.delete(tt.uid)
