# -*- coding:utf-8 -*-

from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabRating
from torcms.model.rating_model import MRating


class TestMRating():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = ''
        self.uid2 = ''
        self.post_id = 'pbp'
        self.userid = 'mqmq'
        self.rating = 3.0

        self.add_message()

    def add_message(self):
        MRating.update(self.post_id, self.userid, self.rating)
        aa = MRating.query_by_post(self.post_id)
        for i in aa:
            if i.user_id == self.userid:
                self.uid = i.uid

    def test_query_by_post(self):

        aa = MRating.query_by_post(self.post_id)
        tf = False
        for i in aa:
            if i.user_id == self.userid:
                assert i.rating == float(self.rating)
                self.uid = i.uid
                tf = True

        assert tf

    def test_query_average_rating(self):

        ave1 = MRating.query_average_rating(self.post_id)
        assert ave1 == self.rating
        MRating.update(self.post_id, 'fin', 4)
        ave = MRating.query_average_rating(self.post_id)
        assert ave 
        aa = MRating.query_by_post(self.post_id)
        for i in aa:
            if i.user_id == 'fin':
                self.uid2 = i.uid
        MHelper.delete(TabRating, self.uid2)

    def test_get_rating(self):

        rat = MRating.get_rating(self.post_id, self.userid)
        assert rat == float(self.rating)

    def test_update(self):

        aa = MRating.query_by_post(self.post_id)
        tf = False
        for i in aa:
            if i.user_id == self.userid:
                assert i.rating == float(self.rating)
                self.uid = i.uid
                tf = True
        assert tf

    def teardown_method(self):
        print("function teardown")
        MHelper.delete(TabRating, self.uid)
        self.uid = ''
