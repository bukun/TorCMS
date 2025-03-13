# -*- coding:utf-8 -*-
from torcms.model.nullify_info_model import MNullifyInfo
from torcms.model.post_model import MPost


class TestMNullifyInfo:
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.post_id = 'r42w2'

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
            'valid': kwargs.get('valid', 0),
        }
        post_id = kwargs.get('post_id', self.post_id)

        MPost.add_or_update(post_id, p_d)

    def test_query_pager_by_valid(self):
        self.add_message()
        aa = MNullifyInfo.query_pager_by_valid()
        tf = False
        for i in aa:
            if i.uid == self.post_id:
                tf = True
        assert tf

    def test_count_of_certain(self):
        aa = MNullifyInfo.count_of_certain()
        self.add_message()
        bb = MNullifyInfo.count_of_certain()
        assert bb == aa + 1

    def teardown_method(self):
        print("function teardown")
        MPost.delete(self.post_id)
        self.uid = ''
