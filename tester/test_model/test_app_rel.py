# -*- coding:utf-8 -*-
from torcms.core import tools
from torcms.model.abc_model import MHelper
from torcms.model.category_model import MCategory
from torcms.model.core_tab import TabRel
from torcms.model.label_model import MLabel
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
from torcms.model.relation_model import MRelation


class TestMRelation:
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.post_id = '66565'
        self.tag_id = '2342'
        self.post_id2 = '89898'
        self.uid = ''
        self.add_tag()
        self.add_2post()
        self.add_rela()

    def add_tag(self, **kwargs):
        post_data = {
            'name': kwargs.get('name', 'category'),
            'slug': kwargs.get('slug', 'kkkooo'),
            'order': kwargs.get('order', '0'),
            'kind': kwargs.get('kind1', '1'),
            'pid': kwargs.get('pid', '0000'),
        }
        tf = MCategory.add_or_update(self.tag_id, post_data)
        assert tf == self.tag_id

    def add_post(self, **kwargs):
        p_d = {
            'title': kwargs.get('title', '一二三'),
            'cnt_md': kwargs.get('cnt_md', 'grgr'),
            'time_create': kwargs.get('time_create', '1992'),
            'time_update': kwargs.get('time_update', '1996070600'),
            'user_name': 'flower',
            'view_count': kwargs.get('view_count', 1),
            'logo': kwargs.get('logo', 'prprprprpr'),
            'memo': kwargs.get('memo', ''),
            'order': kwargs.get('order', '1'),
            'keywords': kwargs.get('keywords', 'sd,as'),
            'extinfo': kwargs.get('extinfo', {}),
            'kind': kwargs.get('kind', '1'),
            'valid': kwargs.get('valid', 1),
        }
        p_id = kwargs['post_uid']

        tt = MPost.add_or_update(p_id, p_d)
        assert tt
        MPost2Catalog.add_record(p_id, self.tag_id)

    def add_2post(self):
        post_data = {
            'post_uid': self.post_id,
            'title': 'sky',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        self.add_post(**post_data)
        post_data2 = {
            'post_uid': self.post_id2,
            'title': 'blue',
            'cnt_md': '## adslsdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        self.add_post(**post_data2)

    def add_rela(self):
        aa = MRelation.add_relation(self.post_id, self.post_id2)
        self.uid = aa

    def test_add_relation(self):
        print('====')
        print(self.uid)
        aa = MHelper.get_by_uid(TabRel, self.uid)
        assert aa.post_f_id == self.post_id
        assert aa.post_t_id == self.post_id2

    def test_update_relation(self):
        MRelation.update_relation(self.post_id, self.post_id2, weight=2)
        aa = MHelper.get_by_uid(TabRel, self.uid)
        assert aa.count >= 2 + 1

    # def test_get_app_relations(self):
    #     self.add_tag()
    #     self.add_2post()
    #     self.add_rela()
    #     aa=MRelation.get_app_relations(self.post_id)
    #     tf=False
    #     for i in aa:
    #         print(i.post_id)
    #         if i.post_id==self.post_id2:
    #             tf=True
    #     self.teardown_class()
    #     assert tf

    def test_delete(self):
        aa = MHelper.get_by_uid(TabRel, self.uid)
        assert aa.post_f_id == self.post_id
        MRelation.delete(self.uid)
        aa = MHelper.get_by_uid(TabRel, self.uid)
        assert aa == None

    def teardown_method(self):
        print("function teardown")
        tt = MCategory.get_by_uid(self.tag_id)
        if tt:
            MCategory.delete(tt.uid)
        aa = MPost.get_by_uid(self.post_id2)
        aa2 = MPost.get_by_uid(self.post_id)
        if aa:
            MPost.delete(self.post_id2)

        if aa2:
            MPost.delete(self.post_id)

        MPost2Catalog.remove_relation(self.post_id, self.tag_id)

        MRelation.delete(self.uid)
        self.uid = ''
