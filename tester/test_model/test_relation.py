# -*- coding:utf-8 -*-
from torcms.model.category_model import MCategory
from torcms.model.label_model import MLabel
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
from torcms.model.relation_model import MRelation


class TestMRelation():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uu = MPost()
        self.m2c = MPost2Catalog()

        self.app_f = 'ddss'
        self.app_t = '6122'

        self.tag_id = '6654'
        self.uid=''
        self.slug = 'huio'

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
            'valid': kwargs.get('valid', 1),

        }
       
        MPost.create_post(self.app_f, p_d)
        MPost2Catalog.add_record(self.app_f, self.tag_id)


        p_d = {
            'title': 'oioi',
            'cnt_md': 'oioi',
            'time_create': '1998',
            'time_update':'1999',
            'user_name': 'oioi',
            'view_count': 1,
            'logo': 'oioi',
            'memo': '',
            'order':1,
            'keywords': '',
            'extinfo': {},
            'kind': "1",
            'valid': 1,

        }

        MPost.create_post(self.app_t, p_d)
        a = MPost.get_by_uid(self.app_t)

        MPost2Catalog.add_record(self.app_t, self.tag_id)


    def test_add_relation(self):
        self.setup()
        self.add_message()
        a=MRelation.add_relation(self.app_f, self.app_t)

        self.uid=a

        assert a
        self.tearDown()

    def test_update_relation(self):
        self.add_message()
        a=MRelation.add_relation(self.app_f, self.app_t)
        self.uid = a
        a =MRelation.update_relation(self.app_f, self.app_t)
        assert a!=False
        self.tearDown()

    def test_get_app_relations(self):

        self.add_message()
        MRelation.add_relation(self.app_f, self.app_t)
        a=MRelation.get_app_relations(self.app_f,num=300)

        tf=False
        for i in a:
            if i.post_id==self.app_f:
                tf=True
        assert tf
        self.tearDown()

    def test_delete(self):
        a = MRelation.add_relation(self.app_f, self.app_t)
        MRelation.update_relation(self.app_f, self.app_t)

        self.uid = a
        MRelation.delete(self.uid)
        au=MRelation.update_relation(self.app_f, self.app_t)
        assert au==False
        self.tearDown()


    def tearDown(self):
        print("function teardown")

        tt = self.uu.get_by_uid(self.app_f)
        if tt:

            MPost2Catalog.remove_relation(self.app_t, self.tag_id)
            MPost2Catalog.remove_relation(self.app_f, self.tag_id)
            MCategory.delete(self.tag_id)

            MPost.delete(self.app_f)
            MPost.delete(self.app_t)


        MRelation.delete(self.uid)
        tt = MLabel.get_by_slug(self.slug)
        if tt:
            MLabel.delete(tt.uid)