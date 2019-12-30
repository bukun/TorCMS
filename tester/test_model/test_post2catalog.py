# -*- coding:utf-8 -*-
from torcms.model.category_model import MCategory
from torcms.model.label_model import MLabel
from torcms.model.post2catalog_model import MPost2Catalog

from torcms.core import tools
from torcms.model.post_model import MPost


class TestMPost2Catalog():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')

        self.post_id = '22222'
        self.tag_id = '1111'
        self.post_id2 = '13122'
        self.slug = 'ssslug'

    def test_add_record(self):
        self.add_message()

        MPost2Catalog.add_record(self.post_id, self.tag_id)
        Po = MPost2Catalog.query_by_post(self.post_id)


        assert Po.count() > 0
        self.tearDown()

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
            'title': kwargs.get('title','iiiii'),
            'cnt_md': kwargs.get('cnt_md','grgr'),
            'time_create': kwargs.get('time_create','1992'),
            'time_update': kwargs.get('time_update','1996'),
            'user_name': kwargs.get('user_name','yuanyuan'),
            'view_count': kwargs.get('view_count','1'),
            'logo': kwargs.get('logo','prprprprpr'),
            'memo': kwargs.get('memo',''),
            'order': kwargs.get('order','1'),
            'keywords': kwargs.get('keywords',''),
            'extinfo':kwargs.get( 'extinfo', {}),
            'kind': kwargs.get('kind2','1'),
            'valid':kwargs.get( 'valid','1'),

        }
        post_id=kwargs.get('post_id',self.post_id)
        i = MPost.get_by_uid(post_id)


        g = MPost.create_post(post_id, p_d)

    def add_P2C(self):
        MPost2Catalog.add_record(self.post_id, self.tag_id)
    def test_just_query_all(self):
        self.add_message()
        self.add_P2C()
        a = MPost2Catalog.just_query_all()
        TF = False

        for i in a:
            if i.post_id == self.post_id:

                TF = True

        assert TF
        self.tearDown()

    def test_query_all(self):
        self.add_message()
        self.add_P2C()
        a = MPost2Catalog.query_all()
        TF=False

        for i in a:
            if i.post_id == self.post_id:

                TF = True

        assert TF
        self.tearDown()

    def test_remove_relation(self):
        self.add_message()
        MPost2Catalog.add_record(self.post_id, self.tag_id)
        MPost2Catalog.remove_relation(self.post_id, self.tag_id)
        a = MPost2Catalog.query_all()
        TF=True

        for i in a:
            if i.post_id == self.post_id:

                TF = False

        assert TF
        self.tearDown()

    def test_remove_tag(self):
        self.add_message()
        self.add_P2C()
        MPost2Catalog.remove_tag(self.tag_id)
        TF=MPost2Catalog.query_by_catid(self.tag_id)

        assert TF.count()==0
        self.tearDown()

    def test_query_by_catid(self):
        self.add_message()
        self.add_P2C()
        b=MPost2Catalog.query_by_catid(self.tag_id)


        assert b[0].post_id==self.post_id
        self.tearDown()

    def test_query_postinfo_by_cat(self):
        self.add_message()
        self.add_P2C()
        ss=MPost2Catalog.query_postinfo_by_cat(self.tag_id)
        assert ss[0].logo=='prprprprpr'
        self.tearDown()

    def test_query_by_post(self):
        self.add_message()
        self.add_P2C()
        ss=MPost2Catalog.query_by_post(self.post_id)
        assert ss[0].tag_id==self.tag_id
        self.tearDown()

    def test_query_count(self):
        self.add_message()
        self.add_P2C()
        ss=MPost2Catalog.query_count()

        TF=False
        for i in ss:
            if i.tag_id==self.tag_id:
                if i.num==1:
                    TF=True
        assert TF
        self.tearDown()

    def test_update_field(self):
        self.add_message()
        self.add_P2C()
        kwargs={
            'post_id':self.post_id2
        }

        self.add_message(**kwargs)
        ss = MPost2Catalog.query_by_post(self.post_id)

        MPost2Catalog.update_field(ss[0].uid, post_id=kwargs['post_id'])
        aa = MPost2Catalog.query_by_post(kwargs['post_id'])

        assert ss[0].uid==aa[0].uid
        self.tearDown()


    def test_count_of_certain_category(self):
        b = MPost2Catalog.count_of_certain_category(self.tag_id)
        self.add_message()
        self.add_P2C()
        a=MPost2Catalog.count_of_certain_category(self.tag_id)


        assert b+1==a
        self.tearDown()

    def test_query_pager_by_slug(self):
        kwargs = {
            'slug': 'awer'
        }

        self.add_message(**kwargs)
        self.add_P2C()
        a=MPost2Catalog.query_pager_by_slug(kwargs['slug'])

        assert a[0].uid==self.post_id
        self.tearDown()

    def test_query_by_entity_uid(self):
        self.add_message()
        self.add_P2C()
        a=MPost2Catalog.query_by_entity_uid(self.post_id)

        assert a[0].tag_id==self.tag_id
        self.tearDown()

    def test_del_by_uid(self):
        self.add_message()
        self.add_P2C()
        ss = MPost2Catalog.query_by_post(self.post_id)
        a=MPost2Catalog.del_by_uid(ss[0].uid)
        assert a
        self.tearDown()

    def test_query_by_id(self):
        self.add_message()
        self.add_P2C()
        a = MPost2Catalog.query_by_id(self.post_id)

        assert a[0].tag_id == self.tag_id
        self.tearDown()


    def test_get_first_category(self):
        self.add_message()
        self.add_P2C()
        a=MPost2Catalog.get_first_category(self.post_id)
        b=MPost2Catalog.del_by_uid(a)

        assert b
        self.tearDown()


    def tearDown(self):
        print("function teardown")
        tt = MCategory.get_by_uid(self.tag_id)
        if tt:
            MCategory.delete(self.tag_id)
        tt = MPost.get_by_uid(self.post_id)
        if tt:
            MPost.delete(self.post_id)


            MPost2Catalog.remove_relation(self.post_id, self.tag_id)
        tt = MPost.get_by_uid(self.post_id2)
        if tt:
            MPost.delete(self.post_id2)


            MPost2Catalog.remove_relation(self.post_id2, self.tag_id)

        tt = MLabel.get_by_slug(self.slug)
        if tt:
            print('8888888888')
            MLabel.delete(self.slug)


