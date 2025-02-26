# -*- coding:utf-8 -*-
import random

from torcms.model.entity2user_model import MEntity2User
from torcms.model.entity_model import MEntity
from torcms.model.user_model import MUser


class TestMEntity2User:
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.M2U = MEntity2User()
        self.username = 'ieee'
        self.uu = MUser()
        self.user_uid = ''
        self.e_uid = 'q112'
        self.path = '/static/123123'
        self.userip = '10.6.0.177'
        self.ee = MEntity()
        self.uid = ''

    def add_user(self, **kwargs):
        name = kwargs.get('user_name', self.username)
        post_data = {
            'user_name': name,
            'user_pass': kwargs.get('user_pass', 'g131322'),
            'user_email': kwargs.get(
                'user_email', '{}@kljhqq.com'.format(random.randint(1, 1000000))
            ),
        }

        self.uu.create_user(post_data)
        aa = self.uu.get_by_name(name)
        assert aa
        self.user_uid = aa.uid

    def add_entity(self):
        desc = 'create entity'
        tf = self.ee.create_entity(self.e_uid, self.path, desc)
        assert tf

    def add_E2U(self):
        self.add_user()
        self.add_entity()
        self.M2U.create_entity2user(self.e_uid, self.user_uid, self.userip)
        tt = self.M2U.query_all()
        assert tt
        for i in tt:
            if i.entity_id == self.e_uid:
                self.uid = i.uid

    def test_get_by_uid(self):
        self.add_E2U()
        tt = self.M2U.get_by_uid(self.uid)
        assert tt.user_ip == self.userip
        assert tt.entity_id == self.e_uid

    def test_delete_by_uid(self):
        self.add_E2U()
        tt = self.M2U.get_by_uid(self.uid)
        assert tt.user_ip == self.userip
        self.M2U.delete_by_uid(self.e_uid)
        tt = self.M2U.query_all()
        tf = True
        for i in tt:
            if i.entity_id == self.e_uid:
                tf = False

        assert tf

    def test_query_all(self):
        tt = self.M2U.query_all()
        tf = True
        for i in tt:
            if i.entity_id == self.e_uid:
                tf = False
        assert tf
        self.add_E2U()
        tt = self.M2U.query_all()
        tf = True
        for i in tt:
            if i.entity_id == self.e_uid:
                tf = True

        assert tf

    def test_get_all_pager(self):
        self.add_E2U()
        aa = self.M2U.query_all(limit=200)
        a = int(aa.count() / 10) + 2
        tf = False
        for i in range(a):
            tt = self.M2U.get_all_pager(current_page_num=i)
            for t in tt:
                if t.uid == self.uid:
                    tf = True
                    assert t.user_id == self.user_uid
                    assert t.user_ip == self.userip

        assert tf

    def test_get_all_pager_by_username(self):
        self.add_E2U()
        tf = False
        aa = self.M2U.get_all_pager_by_username(self.user_uid)
        for t in aa:
            if t.uid == self.uid:
                tf = True
                assert t.user_ip == self.userip

        assert tf

    def test_create_entity2user(self):
        self.add_E2U()
        tt = self.M2U.get_by_uid(self.uid)
        assert tt.user_ip == self.userip

    def test_total_number(self):
        a = self.M2U.total_number()
        self.add_E2U()
        b = self.M2U.total_number()

        assert a + 1 <= b

    def test_total_number_by_user(self):
        self.add_user()
        aa = self.M2U.total_number_by_user(self.user_uid)
        self.add_E2U()
        bb = self.M2U.total_number_by_user(self.user_uid)

        assert aa + 1 <= bb

    def teardown_method(self):
        print("function teardown")
        self.uu.delete_by_user_name(self.username)
        self.ee.delete(self.e_uid)
        self.M2U.delete_by_uid(self.e_uid)
