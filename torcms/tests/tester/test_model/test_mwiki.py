# -*- coding:utf-8 -*-

import tornado.escape

from torcms.core import tools
from torcms.model.wiki_model import MWiki


class TestMWiki:
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.raw_count = MWiki.get_counts()
        self.wiki_title = 'lkablkjcdefg'
        self.wiki_title2 = 'lkablkjcdefgqq'
        self.uid = ""
        self.uid2 = "asdf"
        self.add_mess()

    def add_mess(self):
        p_d = {
            'title': self.wiki_title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
        }
        MWiki.create_wiki(p_d)
        aa = MWiki.get_by_wiki(self.wiki_title)
        self.uid = aa.uid

    def test_insert_1(self):
        '''Wiki insert: Test invalid title'''
        post_data = {
            'title': '',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
        }
        uu = MWiki.create_wiki(post_data)
        assert uu == False

    def test_get_by_title(self):
        ss = MWiki.get_by_uid(self.uid)
        assert ss.title == self.wiki_title
        tt = MWiki.get_by_title(self.wiki_title)
        assert tt.title == self.wiki_title

    def test_get_by_title2(self):
        '''Test Wiki title with SPACE'''

        ss = MWiki.get_by_uid(self.uid)
        assert ss.title == self.wiki_title
        tt = MWiki.get_by_title(self.wiki_title)
        assert tt.title == self.wiki_title.strip()

    def test_upate_by_view_count(self):
        rec = MWiki.get_by_wiki(self.wiki_title)

        viewcount0 = rec.view_count
        assert viewcount0 >= 2
        for x in range(100):
            MWiki.update_view_count_by_uid(rec.uid)

        viewcount1 = MWiki.get_by_wiki(self.wiki_title).view_count
        assert viewcount1 >= 103

    def test_upate(self):
        rec = MWiki.get_by_wiki(self.wiki_title)
        p_d = {
            'title': 'bibibobo',
            'cnt_md': 'dd25d5fd6d',
        }
        MWiki.update(self.uid, p_d)
        now = MWiki.get_by_wiki(p_d['title'])
        assert rec.uid == now.uid
        assert now.uid == self.uid

    def test_get_counts(self):
        a = MWiki.get_counts()

        assert a >= 1

    def test_query_recent_edited(self):
        aa = MWiki.query_recent_edited(111111)
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True
                break

        assert tf

    def test_delete(self):
        tf = False
        aa = MWiki.query_all()
        for i in aa:
            if i.uid == self.uid:
                tf = True
                break
        assert tf
        MWiki.delete(self.uid)
        aa = MWiki.query_all()
        tf = True
        for i in aa:
            if i.title == self.wiki_title:
                tf = False
                break

        assert tf

    def test_get_by_uid(self):
        tf = False
        aa = MWiki.query_all()
        for i in aa:
            if i.uid == self.uid:
                tf = True
                break
        assert tf
        bb = MWiki.get_by_uid(self.uid)
        assert bb.title == self.wiki_title

    def test_update_cnt(self):
        aa = MWiki.get_by_uid(self.uid)
        pf = {'user_name': 'ooqwer', 'cnt_md': 'qwertyuioplkjgfdsa'}
        MWiki.update_cnt(self.uid, pf)
        bb = MWiki.get_by_uid(self.uid)
        assert aa.user_name != bb.user_name
        assert bb.user_name == pf['user_name']

    def test_create_page(self):
        p_d = {
            'title': self.wiki_title2,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
        }
        tf = MWiki.create_page(self.uid2, p_d)
        assert tf == True
        aa = MWiki.get_by_uid(self.uid2)

        assert aa.title == self.wiki_title2
        assert aa.kind == '2'

    def test_query_dated(self):
        aa = MWiki.query_dated(num=100)
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True
                break

        assert tf

    def test_query_most(self):
        aa = MWiki.query_most(num=100)
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True
                break

        assert tf

    def test_update_view_count(self):
        aa = MWiki.get_by_uid(self.uid)
        for i in range(5):
            MWiki.update_view_count(self.wiki_title)
        bb = MWiki.get_by_uid(self.uid)
        assert aa.view_count + 5 <= bb.view_count

    def test_update_view_count_by_uid(self):
        aa = MWiki.get_by_uid(self.uid)
        for i in range(5):
            MWiki.update_view_count_by_uid(self.uid)
        bb = MWiki.get_by_uid(self.uid)
        assert aa.view_count + 5 <= bb.view_count

    def test_get_by_wiki(self):
        aa = MWiki.get_by_wiki(self.wiki_title)
        assert aa.uid == self.uid

    def test_query_all(self):
        aa = MWiki.query_all()
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True
                break

        assert tf

    def test_view_count_plus(self):
        aa = MWiki.get_by_uid(self.uid)
        for i in range(5):
            MWiki.view_count_plus(self.uid)
        bb = MWiki.get_by_uid(self.uid)
        assert aa.view_count + 5 <= bb.view_count

    def test_query_random(self):
        aa = MWiki.query_random(num=50)
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True
                break

        assert tf

    def test_query_recent(self):
        aa = MWiki.query_recent(num=50)
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True
                break

        assert tf

    def test_total_number(self):
        aa = MWiki.total_number('1')

        assert aa >= 1

    def test_query_pager_by_kind(self):
        aa = MWiki.total_number('1')
        a = int(aa / 10) + 2
        tf = False
        for i in range(a):
            x = MWiki.query_pager_by_kind('1', current_page_num=i)
            for y in x:
                if y.uid == self.uid:
                    assert y.title == self.wiki_title
                    tf = True
                    break

        assert tf

    def test_count_of_certain_kind(self):
        aa = MWiki.count_of_certain_kind('1')

        assert aa >= 1

    def teardown_method(self):
        print("function teardown")
        MWiki.delete(self.uid)
        MWiki.delete(self.uid2)
