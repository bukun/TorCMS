# -*- coding:utf-8 -*-
from torcms.model.category_model import MCategory
from torcms.model.evaluation_model import MEvaluation
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost


class TestMEvaluation():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.user_id = '11111'
        self.app_id = 'a1244'
        self.post_id = self.app_id

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

        MPost.add_or_update(post_id, p_d)
        user_id = kwargs.get('user_id', self.user_id)
        MEvaluation.add_or_update(user_id, self.app_id, 1)

    def test_app_evaluation_count(self):
        b = MEvaluation.app_evaluation_count(self.app_id)

        p = {
            'user_id': '33336'
        }
        self.add_message(**p)
        p = {
            'user_id': '54436'
        }
        self.add_message(**p)

        a = MEvaluation.app_evaluation_count(self.app_id)
        assert a == b + 2
        self.teardown_class()

    def test_get_by_signature(self):
        a = MEvaluation.get_by_signature(self.user_id, self.app_id)
        assert a == None
        self.add_message()
        a = MEvaluation.get_by_signature(self.user_id, self.app_id)
        assert a
        self.teardown_class()

    def test_add_or_update(self):
        value = 1
        MEvaluation.add_or_update(self.user_id, self.app_id, value)
        a = MEvaluation.get_by_signature(self.user_id, self.app_id)
        assert a
        self.teardown_class()

    def teardown_class(self):
        print("function teardown")
        MPost.delete(self.post_id)
