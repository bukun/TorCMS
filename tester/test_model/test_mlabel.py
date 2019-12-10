# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.label_model import MLabel
from torcms.model.label_model import MPost2Label
from torcms.model.post_model import MPost


class TestMLabel():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uu = MLabel()
        self.name = 'name'
        self.tmpl_uid = ''
        self.uid = tools.get_uu4d()
        self.post_id='2222'


    def test_create_tag(self):
        post_data = {
            'name': self.name,
        }
        newid = MLabel.create_tag(post_data['name'])

        tt = MLabel.get_id_by_name(post_data['name'])

        self.tmpl_uid = tt
        assert tt == newid



    def test_create_tag_with_uid(self):
        '''Wiki insert: Test invalid title'''
        post_data = {
            'name': self.name,
        }
        self.uu.create_tag_with_uid(self.uid, post_data['name'])
        a=self.uu.get_id_by_name(post_data['name'])
        assert a==self.uid

    def add_message(self, **kwargs):
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

        MPost.create_post(post_id, p_d)
        self.uu.create_tag_with_uid(self.uid, self.name)
        MPost2Label.add_record(self.post_id, self.name)
    #
    # def test_get_id_by_name(self):
    #     self.add_message()
    #     a=self.uu.get_id_by_name(self.name)
    #     print(a)
    #     print(self.uid)
    #     assert a==self.uid

    def test_get_by_slug(self):
        self.add_message()
        a=self.uu.get_by_slug(self.uid)
        assert a.name==self.name

    def test_delete(self):
        self.add_message()
        a = self.uu.get_by_slug(self.uid)
        assert a.name == self.name
        self.uu.delete(self.uid)
        a = self.uu.get_by_slug(self.uid)
        print(a)
        assert a==False

    def tearDown(self):
        print("function teardown")
        tt = self.uu.get_by_slug(self.tmpl_uid)
        if tt:
            print('99999999')
            self.uu.delete(self.tmpl_uid)
        tt = self.uu.get_by_slug(self.uid)
        if tt:
            print('444444444')
            self.uu.delete(self.uid)

        tt = MPost.get_by_uid(self.post_id)
        if tt:
            print('0000000000')
            MPost.delete(self.post_id)


class TestMPost2Label():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')

        self.name = 'nyteame'

        self.uid = '3344'
        self.post_id = 'frwcd'
        self.tag_id = self.uid

    def add_mess(self, **kwargs):
        p_d = {
            'title': kwargs.get('title', 'iiiii'),
            'cnt_md': kwargs.get('cnt_md', 'grgr'),
            'time_create': kwargs.get('time_create', '1992'),
            'time_update': kwargs.get('time_update', '1996070600'),
            'user_name': kwargs.get('user_name', 'fdsa'),
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


        MPost.create_post(post_id, p_d)

        MLabel.create_tag_with_uid(self.uid, self.name)


    def add_M2L(self):
        MPost2Label.add_record(self.post_id, self.name)

    def test_query_count(self):
        self.add_mess()
        a=MPost2Label.query_count(self.uid)

        print( a)
        self.add_M2L()


        b = MPost2Label.query_count(self.uid)
        print(b)
        assert a+1==b

    def test_remove_relation(self):
        self.add_mess()
        self.add_M2L()
        a = MPost2Label.get_by_uid(self.post_id)
        tf = False
        for i in a:

            if i.tag_id == self.tag_id:
                tf = True
        assert tf
        MPost2Label.remove_relation(self.post_id, self.tag_id)
        a = MPost2Label.get_by_uid(self.post_id)
        tf = True
        for i in a:

            if i.tag_id == self.tag_id:
                tf = False
        assert tf
        assert True

    # def test_generate_catalog_list(self):
    #     self.add_mess()
    #     self.add_M2L()
    #     a=MPost2Label.generate_catalog_list(self.post_id)
    #     print(a)
    #     assert a==0

    def test_get_by_uid(self):
        self.add_mess()
        a = MPost2Label.get_by_uid(self.post_id)
        print(a.count())
        assert a.count()==0
        self.add_M2L()
        a = MPost2Label.get_by_uid(self.post_id)

        assert a[0].tag_id==self.uid

    def test_get_by_info(self):
        self.add_mess()
        self.add_M2L()
        a=MPost2Label.get_by_info(self.post_id, self.tag_id)
        assert a!=None

    def test_add_record(self):
        a=MPost2Label.get_by_uid(self.post_id)
        tf=True
        for i in a:
            if i.tag_id==self.tag_id:
                tf=False
        assert tf
        self.add_mess()
        MPost2Label.add_record(self.post_id, self.name)
        a = MPost2Label.get_by_uid(self.post_id)
        tf = False
        for i in a:

            if i.tag_id == self.tag_id:
                tf = True
        assert tf

    def test_total_number(self):
        self.add_mess()
        a=MPost2Label.total_number(self.uid)
        self.add_M2L()
        b=MPost2Label.total_number(self.uid)
        assert a+1==b

    def test_query_pager_by_slug(self):
        self.add_mess()
        self.add_M2L()
        a=MPost2Label.query_pager_by_slug(self.uid)
        print(a)
        print(a.count())

        tf = False
        for i in a:
            print(i)

            if i.uid == self.post_id:
                tf = True
        assert tf

    def tearDown(self):
        print("function teardown")

        tt = MPost.get_by_uid(self.post_id)
        if tt:
            print('777777777777')
            MPost.delete(self.post_id)

        tt=MLabel.get_by_slug(self.tag_id)
        if tt:
            print('8888888888')
            MLabel.delete(self.tag_id)



