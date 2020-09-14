# -*- coding:utf-8 -*-

from torcms.model.referrer_model import MReferrer


class TestMReferrer():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = '',
        self.post_id = 'grww',
        self.userip = '423'

    def add_message(self,**kwargs):
        post_data = {
            'media': kwargs.get('media', 'ffeerrt'),
            'terminal': kwargs.get('terminal', 'lllplplp'),
            'kind': kwargs.get('kind', '1'),
            'userip': kwargs.get('userip', self.userip),
        }
        self.uid=MReferrer.add_meta('ftydd', post_data)

    def test_modify_meta(self):
        self.add_message()
        post_data = {
            'media': 'fffffff',
            'terminal':'4f4f4fgg',
            'kind':'9',
            'userip':'fw3er5'
        }
        MReferrer.modify_meta(self.uid,post_data)
        b = MReferrer.get_by_uid(self.uid)

        assert b.media == post_data['media']
        assert b.terminal == post_data['terminal']
        assert b.kind == post_data['kind']
        assert b.userip == post_data['userip']

        self.tearDown()

    def test_add_meta(self):
        self.add_message()
        b = MReferrer.get_by_userip(self.userip)
        assert b[0].uid==self.uid
        self.tearDown()

    def test_delete(self):
        self.add_message()
        b = MReferrer.get_by_userip(self.userip)
        assert b[0].uid==self.uid
        MReferrer.delete(self.uid)
        b = MReferrer.get_by_userip(self.userip)
        assert b.count() == 0
        self.tearDown()


    def test_query_all(self):
        self.add_message()
        b = MReferrer.query_all()
        for i in b:
            if i.uid==self.uid:
                assert i.userip==self.userip
        self.tearDown()

    def test_get_by_userip(self):
        self.add_message()
        b = MReferrer.get_by_userip(self.userip)
        assert b[0].uid==self.uid
        self.tearDown()

    def test_get_by_uid(self):
        self.add_message()
        b = MReferrer.get_by_uid(self.uid)
        assert b.userip==self.userip
        self.tearDown()

    def tearDown(self):
        print("function teardown")
        MReferrer.delete(self.uid)
        self.uid=''
