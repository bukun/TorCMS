# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.link_model import MLink


class TestMLink:
    def setup_method(self):
        self.id = tools.get_uu4d()
        self.raw_count = MLink.get_counts()
        self.add_message()
        print(self.raw_count)

    def test_create_link(self):
        uid = self.id
        post_data = {
            'name': 'asdf',
            'link': 'sadf',
            'order': '1',
            'logo': 'asf',
        }
        MLink.create_link(uid, post_data)

        new_count = MLink.get_counts()

        tt = MLink.get_by_uid(uid)
        assert tt.name == post_data['name']
        assert tt.link == post_data['link']
        assert tt.order == int(post_data['order'])
        assert tt.logo == post_data['logo']
        assert self.raw_count + 1 <= new_count

    def add_message(self, **kwargs):
        uid = self.id
        post_data = {
            'name': kwargs.get('name', 'asdf'),
            'link': kwargs.get('link', 'sadf'),
            'order': kwargs.get('order', '1'),
            'logo': kwargs.get('logo', 'asf'),
        }
        MLink.create_link(uid, post_data)

    def test_upate(self):
        post_data = {
            'name': 'fffffff',
            'link': '85tgr4ggbf',
            'order': '13',
            'logo': 'fdef',
        }
        self.add_message(**post_data)
        new_count = MLink.get_counts()

        assert self.raw_count + 1 <= new_count

        post_data2 = {
            'name': 'asdlkjf',
            'link': 'sakljdf',
            'order': '12',
            'logo': 'asfa',
        }

        MLink.update(self.id, post_data2)

        new_count = MLink.get_counts()

        assert self.raw_count + 1 <= new_count

        tt = MLink.get_by_uid(self.id)

        assert tt.name != post_data['name']
        assert tt.link != post_data['link']
        assert tt.order != int(post_data['order'])
        assert tt.logo != post_data['logo']

        assert tt.name == post_data2['name']
        assert tt.link == post_data2['link']
        assert tt.order == int(post_data2['order'])
        assert tt.logo == post_data2['logo']

    def test_query_all(self):
        a = MLink.query_all()
        tf = False
        for i in a:
            if i.uid == self.id:
                tf = True
        assert tf

    def test_get_by_uid(self):
        a = MLink.get_by_uid(self.id)

        assert a.uid == self.id

    def test_delete(self):
        a = MLink.get_by_uid(self.id)
        assert a.uid == self.id
        MLink.delete(self.id)
        a = MLink.get_by_uid(self.id)
        assert a == None

    def test_get_counts(self):
        a = MLink.get_counts()

        assert a

    def test_query_link(self):
        a = MLink.query_link(29)
        tf = False
        for i in a:
            if i.uid == self.id:
                tf = True
        assert tf

    def teardown_method(self):
        print("function teardown")
        tt = MLink.get_by_uid(self.id)
        if tt:
            MLink.delete(tt.uid)
