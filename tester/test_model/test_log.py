# -*- coding:utf-8 -*-

from config import CMS_CFG
from torcms.core import tools
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabLog
from torcms.model.log_model import MLog


class TestMLog:
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uid = ''
        self.userid = '1lioio'

    def add_message(self, **kwargs):
        post_data = {
            # 'uid': self.uid,
            'url': kwargs.get('url', 'http://87437483'),
            'refer': 'http://232323',
            'user_id': kwargs.get('user_id', self.userid),
            'timein': '1545104860000',
            'timeOut': '1545104861000',
            'timeon': '1',
        }
        a = MLog.add(post_data)
        assert a
        self.uid = a

    def test_add(self):
        a = MLog.query_pager_by_user(self.userid)
        assert a.count() == 0
        post_data = {
            'uid': self.uid,
            'url': 'http://54243243',
            'refer': 'http://344343',
            'user_id': self.userid,
            'timein': '1545104860000',
            'timeOut': '1545104861000',
            'timeon': '1',
        }

        a = MLog.add(post_data)
        self.uid = a

        assert a

    def test_query_pager_by_user(self):
        self.add_message()
        a = MLog.query_pager_by_user(self.userid)
        assert a
        assert a[0].uid == self.uid

    def test_query_all_user(self):
        self.add_message()
        a = MLog.query_all_user()
        assert a
        tf = False
        for i in a:
            if i.uid == self.uid:
                tf = True
        assert tf

    # def test_query_all(self):
    #
    #     p = {
    #         'user_id': ''
    #     }
    #     self.add_message(**p)
    #     a = MLog.query_all_current_url()
    #     x = int(a.count() / CMS_CFG['list_num'])
    #     tf = False
    #     for y in range(x + 3):
    #         a = MLog.query_all(current_page_num=y)
    #         # print(a[0])
    #         for i in a:
    #             print(i.uid)
    #             if i.uid == self.uid:
    #                 tf = True
    #                 break
    #
    #
    #     assert tf

    def test_query_all_pageview(self):
        self.add_message()
        a = MLog.query_all_current_url()
        assert a
        x = int(a.count() / 10)

        tf = False
        for y in range(x + 3):
            a = MLog.query_all_pageview(current_page_num=y)

            for i in a:
                if i.uid == self.uid:
                    tf = True
                    break

        assert tf

    def test_query_all_current_url(self):
        self.add_message()
        a = MLog.query_all_current_url()
        assert a
        tf = False
        for i in a:
            if i.uid == self.uid:
                tf = True

        assert tf

    def test_count_of_current_url(self):
        p = {'url': 'http://10101010101'}

        self.add_message(**p)
        a = MLog.count_of_current_url(p['url'])
        assert a >= 1

    def test_total_number(self):
        a = MLog.total_number()
        assert a != None
        self.add_message()
        b = MLog.total_number()
        assert b
        assert a >= b - 1

    def test_count_of_certain(self):
        a = MLog.count_of_certain(self.userid)
        assert a != None
        self.add_message()
        b = MLog.count_of_certain(self.userid)
        assert b
        assert a >= b - 1

    def test_count_of_certain_pageview(self):
        a = MLog.count_of_certain_pageview()
        assert a != None
        self.add_message()
        b = MLog.count_of_certain_pageview()
        assert b
        assert a >= b - 1

    def test_get_by_uid(self):
        p = {'url': 'http://10101010101'}

        self.add_message(**p)
        a = MLog.get_by_uid(self.uid)
        assert a
        assert a.current_url == p['url']

    def test_get_pageview_count(self):
        p = {'url': 'http://10101010101'}
        b = MLog.get_pageview_count(p['url'])
        assert b != None
        self.add_message(**p)
        a = MLog.get_pageview_count(p['url'])
        assert a
        assert a >= b + 1

    def teardown_method(self):
        print("function teardown")
        tt = MLog.get_by_uid(self.uid)
        if tt:
            MHelper.delete(TabLog, self.uid)
