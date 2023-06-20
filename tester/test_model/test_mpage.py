# -*- coding:utf-8 -*-
import time

import tornado.escape

from torcms.core import tools
from torcms.model.wiki_model import MWiki


class TestMWiki():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uu = MWiki()
        self.title = 'tyyyitle'
        self.uid = '6985'

    def add_page(self, **kwargs):
        post_data = {
            'title': kwargs.get('title', self.title),
            'user_name': kwargs.get('user_name', 'Tome'),
            'cnt_md': kwargs.get('cnt_md', '## adslkfjasdf\n lasdfkjsadf'),

        }
        self.uu.create_page(self.uid, post_data)

    def test_insert(self):
        raw_count = self.uu.get_counts()
        post_data = {
            'title': 'tyyyitle',
            'user_name': 'Tome',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',

        }
        self.add_page(**post_data)
        new_count = self.uu.get_counts()

        tt = self.uu.get_by_uid(self.uid)

        assert tt.title == post_data['title']
        assert tt.cnt_md == tornado.escape.xhtml_unescape(post_data['cnt_md'])
        assert raw_count + 1 <= new_count



    # def test_insert_2(self):
    #
    #     '''Wiki insert: Test invalid title'''
    #     post_data = {
    #         'title': '',
    #         'user_name': 'Tome',
    #         'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
    #
    #     }
    #     aa=self.uu.create_page(self.uid, post_data)
    #     assert aa==False
    #
    #



    def test_query_all(self):
        self.add_page()
        p = {
            'kind': '2'
        }
        aa = self.uu.query_all(**p)
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True

        assert tf

    def test_get_by_slug(self):
        self.add_page()
        aa = self.uu.get_by_uid(self.uid)
        assert aa.title == self.title


    def test_update_cnt(self):
        self.add_page()
        post_data = {
            'user_name': 'name',
            'cnt_md': '## adslkfjgggfdffasdf\n lasdfkjsadf',

        }
        self.uu.update_cnt(self.uid, post_data)
        tt = self.uu.get_by_uid(self.uid)
        assert tt.user_name == post_data['user_name']
        assert tt.cnt_md == tornado.escape.xhtml_unescape(post_data['cnt_md'])


    def test_update(self):
        self.add_page()
        post_data = {
            'title': 'ti',
            'user_name': 'Tome',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
        }
        aa = self.uu.update(self.uid, post_data)
        assert aa == None
        post_data2 = {
            'title': 'tgrgri',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
        }
        self.uu.update(self.uid, post_data2)
        aa = self.uu.get_by_uid(self.uid)
        assert aa.title == post_data2['title']


    def test_query_recent_edited(self):
        timstamp = tools.timestamp()
        time.sleep(1)
        self.add_page()
        aa = self.uu.query_recent_edited(timstamp, kind='2')
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True 
        assert tf

    def teardown_method(self):
        print("function teardown")
        self.uu.delete(self.uid)
