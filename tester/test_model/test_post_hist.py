# -*- coding:utf-8 -*-
from torcms.core import tools
from torcms.model.post_hist_model import MPostHist
from torcms.model.post_model import MPost


class TestMPostHist():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = ''
        self.post_id = 'llk8'

    def test_create_post_history(self):
        

        p_d = {
            'title': 'qqqii',
            'cnt_md': 'qwqwqw',
            'time_create': '1999',
            'time_update': '2019',
            'user_name': 'max',
            'view_count': '1',
            'logo': 'opps',
            'memo': '',
            'order': '1',
            'kind': '1',
            'valid': 1,

        }
        MPost().add_or_update_post(self.post_id, p_d)
        aa = MPost.get_by_uid(self.post_id)
        tf = MPostHist.create_post_history(aa, aa)
        assert tf
        His = MPostHist.query_by_postid(self.post_id)

        self.uid = His[0].uid
        assert His[0].cnt_md == p_d['cnt_md']
        

    def addHis(self, **kwargs):
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
            'kind': kwargs.get('kind', '1'),
            'valid': kwargs.get('valid', 1),

        }
        MPost().add_or_update_post(self.post_id, p_d)
        aa = MPost.get_by_uid(self.post_id)
        MPostHist.create_post_history(aa, aa)

        His = MPostHist.query_by_postid(self.post_id)

        self.uid = His[0].uid

    def test_get_by_uid(self):
        p_t = {
            'cnt_md': 'bbrreedd'
        }
        self.addHis(**p_t)
        pp = MPostHist.get_by_uid(self.uid)
        assert pp.cnt_md == p_t['cnt_md']
        

    def test_update_cnt(self):
        self.addHis()
        post_data = {
            'user_name': 'giser',
            'cnt_md': 'gisersdfsdfsdf'
        }
        MPostHist.update_cnt(self.uid, post_data)
        pp = MPostHist.get_by_uid(self.uid)
        assert pp.cnt_md == post_data['cnt_md']
        

    def test_query_by_postid(self):
        p_t = {
            'cnt_md': 'bbrreedd',
            'user_name': 'ggggbabybaby'
        }
        self.addHis(**p_t)
        aa = MPostHist.query_by_postid(self.post_id)
        assert aa[0].cnt_md == p_t['cnt_md']
        assert aa[0].user_name == p_t['user_name']
        

    def test_get_last(self):
        p_t = {
            'cnt_md': 'bbrreedd',
            'user_name': 'snow'
        }
        self.addHis(**p_t)
        aa = MPostHist.get_last(self.post_id)

        assert aa.user_name == p_t['user_name']
        

    def test_delete(self):
        aa = MPostHist.get_by_uid(self.uid)

        assert aa == None
        self.addHis()
        aa = MPostHist.get_by_uid(self.uid)
        assert aa.post_id == self.post_id
        aa = MPostHist.delete(self.post_id)
        assert aa == False
        

    def teardown_method(self):
        print("function teardown")
        tt = MPostHist.get_by_uid(self.uid)
        if tt:
            MPostHist.delete(tt.uid)
        tt = MPost.get_by_uid(self.post_id)
        if tt:
            MPost.delete(tt.uid)
