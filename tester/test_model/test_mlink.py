# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.link_model import MLink


class TestUM():
    def setup(self):

        self.id = tools.get_uu4d()
        self.raw_count = MLink.get_counts()
        print(self.raw_count)

    def test_insert(self):
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
        assert self.raw_count + 1 == new_count

    def test_upate(self):
        uid = self.id
        post_data = {
            'name': 'asdf',
            'link': 'sadf',
            'order': '1',
            'logo': 'asf',
        }
        MLink.create_link(uid, post_data)
        new_count = MLink.get_counts()

        assert self.raw_count + 1 == new_count

        post_data2 = {

            'name': 'asdlkjf',
            'link': 'sakljdf',
            'order': '13',
            'logo': 'asfa',
        }

        MLink.update(uid, post_data2)

        new_count = MLink.get_counts()

        assert self.raw_count + 1 == new_count

        tt = MLink.get_by_uid(uid)

        assert tt.name != post_data['name']
        assert tt.link != post_data['link']
        assert tt.order != int(post_data['order'])
        assert tt.logo != post_data['logo']

        assert tt.name == post_data2['name']
        assert tt.link == post_data2['link']
        assert tt.order == int(post_data2['order'])
        assert tt.logo == post_data2['logo']

    def tearDown(self):
        MLink.delete(self.id)
