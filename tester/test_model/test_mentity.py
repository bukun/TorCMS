# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.entity_model import MEntity


class TestMEntity:
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = tools.get_uu4d()
        self.path = 'path'
        self.kind = '1'
        self.desc = 'desc'

    def add_message(self, **kwargs):
        uid = kwargs.get('uid', self.uid)
        path = kwargs.get('path', self.path)
        kind = kwargs.get('kind', self.kind)
        desc = kwargs.get('desc', self.desc)

        tt = MEntity.create_entity(uid, path, desc, kind)
        assert tt

    def test_create_entity(self):
        uid = self.uid
        post_data = {
            'path': self.path,
        }

        tf = MEntity.create_entity(uid, post_data['path'])
        assert tf

    def test_create_entity_2(self):
        '''Wiki insert: Test invalid title'''
        post_data = {
            'path': '',
        }
        MEntity.create_entity(self.uid, post_data['path'], self.desc, self.kind)
        uu = MEntity.get_id_by_impath(post_data['path'])

        assert uu == None

    def test_get_by_uid(self):
        self.add_message()
        tf = MEntity.get_by_uid(self.uid)
        assert tf.uid == self.uid

    def test_query_all(self):
        self.add_message()
        tf = MEntity.query_all()
        assert tf != None

    def test_get_by_kind(self):
        post_data = {'kind': '2'}
        self.add_message(**post_data)
        tf = MEntity.get_by_kind('2')
        assert tf

    def test_get_all_pager(self):
        self.add_message()
        tf = MEntity.get_all_pager()
        assert tf

    def test_get_id_by_impath(self):
        self.add_message()

        tf = MEntity.get_id_by_impath(self.path)
        assert tf

    def test_total_number(self):
        self.add_message()

        tf = MEntity.total_number()
        assert tf

    def test_delete(self):
        self.add_message()

        MEntity.delete(self.uid)
        tf = MEntity.get_by_uid(self.uid)
        assert tf is None

    def test_delete_by_path(self):
        self.add_message()

        MEntity.delete_by_path(self.path, kind='1')

        tf = MEntity.get_id_by_impath(self.path)
        assert tf is None

    def teardown_method(self):
        print("function teardown")
        tt = MEntity.get_id_by_impath(self.path)
        if tt:
            MEntity.delete(tt.uid)
