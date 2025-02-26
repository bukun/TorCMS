# -*- coding:utf-8 -*-

from torcms.model.referrer_model import MReferrer


class TestMReferrer:
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = ''
        self.post_id = 'grww'
        self.userip = '423'
        self.add_message()

    def add_message(self, **kwargs):
        post_data = {
            'media': kwargs.get('media', 'ffeerrt'),
            'terminal': kwargs.get('terminal', 'lllplplp'),
            'kind': kwargs.get('kind', '1'),
            'userip': kwargs.get('userip', self.userip),
        }
        self.uid = MReferrer.add_meta('ftydd', post_data)

    def test_modify_meta(self):
        post_data = {
            'media': 'fffffff',
            'terminal': '4f4f4fgg',
            'kind': '9',
            'userip': 'fw3er5',
        }
        MReferrer.modify_meta(self.uid, post_data)
        b = MReferrer.get_by_uid(self.uid)

        assert b.media == post_data['media']
        assert b.terminal == post_data['terminal']
        assert b.kind == post_data['kind']
        assert b.userip == post_data['userip']

    def test_add_meta(self):
        b = MReferrer.get_by_userip(self.userip)
        assert b[0].uid == self.uid

    def test_delete(self):
        b = MReferrer.get_by_userip(self.userip)
        assert b[0].uid == self.uid
        MReferrer.delete(self.uid)
        b = MReferrer.get_by_userip(self.userip)
        assert b.count() == 0

    def test_query_all(self):
        b = MReferrer.query_all()
        for i in b:
            if i.uid == self.uid:
                assert i.userip == self.userip

    def test_get_by_userip(self):
        b = MReferrer.get_by_userip(self.userip)
        assert b[0].uid == self.uid

    def test_get_by_uid(self):
        b = MReferrer.get_by_uid(self.uid)
        assert b.userip == self.userip

    def teardown_method(self):
        print("function teardown")
        MReferrer.delete(self.uid)
        self.uid = ''
