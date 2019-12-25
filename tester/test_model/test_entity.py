# -*- coding:utf-8 -*-
from torcms.core import tools
from torcms.model.entity_model import MEntity


class TestMEntity():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = tools.get_uuid()
        self.path = '/static/123123'

    def test_create_entity(self):
        uid = self.uid
        path = self.path
        desc = 'create entity'
        kind = 'f'
        tt = MEntity.create_entity(uid, path, desc, kind)
        assert tt == True
        self.tearDown()

    def add_message(self):
        desc = 'create entity'
        kind = 'f'
        MEntity.create_entity(self.uid, self.path, desc, kind)

    def test_query_recent(self):
        a=MEntity.get_by_uid(self.uid)
        assert a==None
        self.add_message()
        a = MEntity.get_by_uid(self.uid)
        assert a
        self.tearDown()

    def test_query_all(self):
        self.add_message()
        a=MEntity.query_all()
        tf = False

        for i in a:

            if i.uid == self.uid:
                tf = True
        assert tf
        self.tearDown()

    def test_get_by_kind(self):
        self.add_message()
        a=MEntity.get_by_kind(kind='f' )

        tf = False
        for i in a:
            if i.uid == self.uid:
                tf = True
        assert tf
        self.tearDown()

    def test_get_all_pager(self):
        a = MEntity.get_all_pager()
        tf = True
        for i in a:
            if i.uid == self.uid:
                tf = False
        assert tf
        self.add_message()
        a=MEntity.get_all_pager()
        tf=False
        for i in a:
            if i.uid == self.uid:
                tf=True
        assert tf
        self.tearDown()

    def test_get_id_by_impath(self):
        self.add_message()
        path = self.path
        a=MEntity.get_id_by_impath(path)
        assert a.uid==self.uid
        self.tearDown()

    def test_total_number(self):
        b = MEntity.total_number()

        self.add_message()
        a=MEntity.total_number()

        assert b+1<=a
        self.tearDown()

    def test_delete_by_path(self):
        tf= MEntity.get_by_uid(self.uid)
        assert tf==None
        self.add_message()
        tf= MEntity.get_by_uid(self.uid)
        assert tf
        MEntity.delete_by_path(self.path)
        tf = MEntity.get_by_uid(self.uid)

        assert tf == None
        self.tearDown()

    def test_delete(self):
        tf = MEntity.get_by_uid(self.uid)
        assert tf == None
        self.add_message()
        tf =MEntity.delete(self.uid)
        assert tf
        tf = MEntity.get_by_uid(self.uid)

        assert tf == None
        self.tearDown()

    def tearDown(self):
        print("function teardown")
        tt = MEntity.get_by_uid(self.uid)
        if tt:
            MEntity.delete(tt.uid)
