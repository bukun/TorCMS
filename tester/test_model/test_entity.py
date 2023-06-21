# -*- coding:utf-8 -*-
from torcms.core import tools
from torcms.model.entity_model import MEntity


class TestMEntity():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = tools.get_uuid()
        self.path = '/static/123123'
        self.kind = 'f'
        self.desc = 'create entity'
    def test_create_entity(self):

        tt = MEntity.create_entity(self.uid, self.path, self.desc, self.kind)
        assert tt == True


    def add_message(self):
        tf = MEntity.create_entity(self.uid, self.path, self.desc, self.kind)
        assert tf


    def test_query_recent(self):
        a = MEntity.get_by_uid(self.uid)
        assert a == None
        self.add_message()
        a = MEntity.get_by_uid(self.uid)
        assert a.uid == self.uid
        

    def test_query_all(self):
        self.add_message()
        
        a = MEntity.query_all()
        tf = False

        for i in a:

            if i.uid == self.uid:
                tf = True
        assert tf
        

    def test_get_by_kind(self):
        self.add_message()
        
        a = MEntity.get_by_kind(kind='f')

        tf = False
        for i in a:
            if i.uid == self.uid:
                tf = True
        assert tf
        

    def test_get_all_pager(self):
        a = MEntity.get_all_pager()
        tf = True
        for i in a:
            if i.uid == self.uid:
                tf = False
        assert tf
        self.add_message()
        
        a = MEntity.get_all_pager()
        tf = False
        for i in a:
            if i.uid == self.uid:
                tf = True
        assert tf
        

    def test_get_id_by_impath(self):
        self.add_message()
        
        path = self.path
        a = MEntity.get_id_by_impath(path)
        assert a.uid == self.uid
        

    def test_total_number(self):
        b = MEntity.total_number()

        self.add_message()
        
        a = MEntity.total_number()

        assert b + 1 <= a
        

    def test_delete_by_path(self):
        tf = MEntity.get_by_uid(self.uid)
        assert tf == None
        self.add_message()
        tf = MEntity.get_by_uid(self.uid)
        assert tf
        MEntity.delete_by_path(self.path)
        tf = MEntity.get_by_uid(self.uid)

        assert tf == None
        

    def test_delete(self):
        tf = MEntity.get_by_uid(self.uid)
        assert tf == None
        self.add_message()
        
        tf = MEntity.delete(self.uid)
        assert tf
        tf = MEntity.get_by_uid(self.uid)

        assert tf == None
        

    def teardown_method(self):
        print("function teardown")
        tt = MEntity.get_by_uid(self.uid)
        if tt:
            MEntity.delete(tt.uid)
