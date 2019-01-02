# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.log_model import MLog


class TestMLog():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = tools.get_uu4d()

    def test_insert(self):
        post_data = {
            'url': 'http://',
            'refer': 'http://',
            'user_id': '',
            'timein': '1545104860000',
            'timeOut': '1545104861000',
            'timeon': '1',
        }

        MLog.add(post_data)
        assert True
