# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.log_model import MLog


class TestMLog():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = tools.get_uu4d()

    def test_insert(self):
        post_data = {
            'uid': self.uid,
            'url': 'http://',
            'refer': 'http://',
            'user_id': '',
            'timein': '1545104860000',
            'timeOut': '1545104861000',
            'timeon': '1',
        }

        MLog.add(post_data)
        assert True

    def test_query_all_user(self):
        MLog.query_all_user()
        assert True

    def test_query_all(self):
        MLog.query_all()
        assert True

    def test_query_all_pageview(self):
        MLog.query_all_pageview()
        assert True

    def test_query_all_current_url(self):
        MLog.query_all_current_url()
        assert True

    def test_count_of_current_url(self):
        MLog.count_of_current_url('')
        assert True

    def test_total_number(self):
        MLog.total_number()
        assert True

    def test_count_of_certain(self):
        MLog.count_of_certain('None')
        assert True



