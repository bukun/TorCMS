# -*- coding:utf-8 -*-
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
from torcms.model.relation_model import MRelation


class TestMRelation():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uu = MPost()
        self.m2c = MPost2Catalog()
        self.post_id = '66565'

        self.post_id2 = '89898'
        self.app_f = '13325'
        self.app_t = '61252'

        self.tag_id = '6654'
        self.uid=''

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

       
    def test_add_relation(self):
        a=MRelation.add_relation(self.app_f, self.app_t)
        self.uid=a

        assert a

    def test_update_relation(self):
        a=MRelation.add_relation(self.app_f, self.app_t)
        self.uid = a
        a =MRelation.update_relation(self.app_f, self.app_t)
        assert a!=False

    def test_get_app_relations(self):

        self.add_message()
        a=MRelation.get_app_relations(self.post_id,num=300)

        tf=False
        for i in a:
            if i.post_id==self.post_id:
                tf=True
        assert tf

    def test_delete(self):
        a = MRelation.add_relation(self.app_f, self.app_t)
        self.uid = a
        MRelation.delete(self.uid)
        a=MRelation.update_relation(self.app_f, self.app_t)
        assert a==False


    def tearDown(self):
        print("function teardown")

        tt =  self.uu.get_by_uid(self.post_id)
        if tt:
            MCategory.delete(self.tag_id)

            MPost.delete(self.post_id2)
            MPost.delete(self.post_id)

            MPost2Catalog.remove_relation(self.post_id, self.tag_id)

        MRelation.delete(self.uid)