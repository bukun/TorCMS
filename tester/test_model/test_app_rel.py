# -*- coding:utf-8 -*-
from torcms.model.category_model import MCategory
from torcms.model.label_model import MLabel
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabRel
from torcms.model.relation_model import MRelation
from torcms.core import tools


class TestMRelation():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.post_id = '66565'
        self.tag_id = '2342'
        self.post_id2 = '89898'
        self.uid=''

    def add_tag(self,**kwargs):
        post_data = {
            'name': kwargs.get('name', 'category'),
            'slug': kwargs.get('slug', 'kkkooo'),
            'order': kwargs.get('order', '0'),
            'kind': kwargs.get('kind1', '1'),
            'pid': kwargs.get('pid', '0000'),
        }
        MCategory.add_or_update(self.tag_id, post_data)

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
        p_id=kwargs['post_uid']

        MPost.create_post(p_id, p_d)
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
        aa=MRelation.add_relation(self.post_id, self.post_id2)
        self.uid=aa

    def test_add_relation(self):
        self.add_tag()
        self.add_2post()
        self.add_rela()
        aa=MHelper.get_by_uid(TabRel,self.uid)
        assert aa.post_f_id==self.post_id
        assert aa.post_t_id==self.post_id2
        self.tearDown()


    def test_update_relation(self):
        self.add_tag()
        self.add_2post()
        self.add_rela()
        MRelation.update_relation(self.post_id, self.post_id2,weight=2)
        aa = MHelper.get_by_uid(TabRel, self.uid)
        assert aa.count>=2+1
        self.tearDown()

    def test_get_app_relations(self):
        self.add_tag()
        self.add_2post()
        self.add_rela()
        aa=MRelation.get_app_relations(self.post_id)
        tf=False
        for i in aa:
            print(i.post_id)
            if i.post_id==self.post_id2:
                tf=True
        self.tearDown()
        assert tf


    def test_delete(self):
        self.add_tag()
        self.add_2post()
        self.add_rela()
        aa=MHelper.get_by_uid(TabRel,self.uid)
        assert aa.post_f_id==self.post_id
        MRelation.delete(self.uid)
        aa = MHelper.get_by_uid(TabRel, self.uid)
        assert aa==None
        self.tearDown()

    def tearDown(self):
        MCategory.delete(self.tag_id)
        MPost.delete(self.post_id2)
        MPost.delete(self.post_id)

        MPost2Catalog.remove_relation(self.post_id, self.tag_id)

        MRelation.delete(self.uid)
