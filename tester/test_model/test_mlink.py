# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.mlink import MLink

print('hello')


def test_mlink_insert():
    ''' Test mlink insert '''
    # assert 0
    uu = MLink()
    uid = tools.get_uu4d()
    raw_count = uu.get_counts()

    post_data = {
        'name': ['asdf'],
        'link': ['sadf'],
        'order': ['1'],
        'logo': ['asf'],
    }
    uu.insert_data(uid, post_data)
    new_count = uu.get_counts()

    tt = uu.get_by_uid(uid)
    # assert
    assert tt.name == post_data['name'][0]
    assert tt.link == post_data['link'][0]
    assert tt.order == int(post_data['order'][0])
    assert tt.logo == post_data['logo'][0]
    assert raw_count + 1 == new_count

    uu.delete(uid)


class TestUM():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uu = MLink()
        self.id = tools.get_uu4d()
        self.raw_count = self.uu.get_counts()
        print(self.raw_count)

    def test_insert(self):


        uid = self.id
        post_data = {
            'name': ['asdf'],
            'link': ['sadf'],
            'order': ['1'],
            'logo': ['asf'],
        }
        self.uu.insert_data(uid, post_data)

        new_count = self.uu.get_counts()

        tt = self.uu.get_by_uid(uid)
        # assert
        assert tt.name == post_data['name'][0]
        assert tt.link == post_data['link'][0]
        assert tt.order == int(post_data['order'][0])
        assert tt.logo == post_data['logo'][0]
        assert  self.raw_count + 1 == new_count

    def test_upate(self):
        uid = self.id
        post_data = {
            'name': ['asdf'],
            'link': ['sadf'],
            'order': ['1'],
            'logo': ['asf'],
        }
        self.uu.insert_data(uid, post_data)
        new_count = self.uu.get_counts()

        assert self.raw_count + 1 == new_count

        post_data2 = {

            'name': ['asdlkjf'],
            'link': ['sakljdf'],
            'order': ['13'],
            'logo': ['asfa'],
        }

        self.uu.update(uid, post_data2)

        new_count = self.uu.get_counts()

        assert self.raw_count + 1 == new_count

        tt = self.uu.get_by_uid(uid)

        assert tt.name != post_data['name'][0]
        assert tt.link != post_data['link'][0]
        assert tt.order != int(post_data['order'][0])
        assert tt.logo != post_data['logo'][0]

        assert tt.name == post_data2['name'][0]
        assert tt.link == post_data2['link'][0]
        assert tt.order == int(post_data2['order'][0])
        assert tt.logo == post_data2['logo'][0]

    def tearDown(self):
        print ("function teardown")
        self.uu.delete(self.id)
