# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.wiki_model import MWiki
import tornado.escape


class TestMWiki():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.raw_count = MWiki.get_counts()
        self.wiki_title = 'lkablkjcdefg'
        self.uid=""

    def add_mess(self,**kwargs):
        p_d = {
            'title': self.wiki_title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',

        }
        MWiki.create_wiki(p_d)
        aa = MWiki.get_by_wiki(self.wiki_title)
        self.uid = aa.uid


    def test_insert(self):
        raw_count = MWiki.get_counts()
        self.add_mess()
        new_count = MWiki.get_counts()

        tt = MWiki.get_by_wiki(self.wiki_title)

        assert tt.title == self.wiki_title
        assert raw_count + 1 <= new_count
        self.tearDown()

    def test_insert_2(self):
        '''Wiki insert: Test invalid title'''
        post_data = {
            'title': '',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
        }
        uu = MWiki.create_wiki(post_data)
        assert uu == None


    def test_get_by_title(self):
        self.add_mess()
        ss = MWiki.get_by_uid(self.uid)
        assert ss.title == self.wiki_title
        tt = MWiki.get_by_title(self.wiki_title)
        assert tt.title == self.wiki_title
        self.tearDown()

    def test_get_by_title2(self):
        '''Test Wiki title with SPACE'''
        post_data = {
            'title': '  ' + self.wiki_title + '  ',

        }
        self.add_mess(**post_data)
        ss = MWiki.get_by_uid(self.uid)
        assert ss.title == self.wiki_title
        tt = MWiki.get_by_title(self.wiki_title)
        assert tt.title == post_data['title'].strip()
        self.tearDown()

    def test_upate_by_view_count(self):
        self.add_mess()
        rec = MWiki.get_by_wiki(self.wiki_title)

        viewcount0 = rec.view_count
        assert viewcount0 >= 2
        for x in range(100):
            MWiki.update_view_count_by_uid(rec.uid)

        viewcount1 = MWiki.get_by_wiki(self.wiki_title).view_count
        assert viewcount1 >= 103

        self.tearDown()

    def test_upate(self):
        self.add_mess()
        rec = MWiki.get_by_wiki(self.wiki_title)
        p_d = {
            'title': 'bibibobo',
            'cnt_md': 'dd25d5fd6d',
            }
        MWiki.update(self.uid,p_d)
        now=MWiki.get_by_wiki(p_d['title'])
        assert rec.uid==now.uid
        assert now.uid==self.uid
        self.tearDown()


    def test_get_counts(self):
        a=MWiki.get_counts()
        self.add_mess()
        b=MWiki.get_counts()
        assert a+1<=b
        self.tearDown()

    # def test_query_recent_edited(self):
    #     MWiki.query_recent_edited()

    # def test_delete(self):
    #     MWiki.delete()
    #
    # def test_get_by_uid(self):
    #     MWiki.get_by_uid()
    # def test_update_cnt(self):
    #     MWiki.update_cnt()
    #
    # def test_create_page(self):
    #     MWiki.create_page()
    #
    # def test_query_dated(self):
    #     MWiki.query_dated()
    #
    # def test_query_most(self):
    #     MWiki.query_most()
    #
    #
    # def test_update_view_count(self):
    #     MWiki.update_view_count()
    #
    # def test_update_view_count_by_uid(self):
    #     MWiki.update_view_count_by_uid()
    #
    # def test_get_by_wiki(self):
    #     MWiki.get_by_wiki()
    #
    # def test_query_all(self):
    #     MWiki.query_all()
    #
    # def test_view_count_plus(self):
    #     MWiki.view_count_plus()
    #
    # def test_query_random(self):
    #     MWiki.query_random()
    #
    # def test_query_recent(self):
    #     MWiki.query_recent()
    #
    # def test_total_number(self):
    #     MWiki.total_number()
    #
    # def test_query_pager_by_kind(self):
    #     MWiki.query_pager_by_kind()
    #
    # def test_count_of_certain_kind(self):
    #     MWiki.count_of_certain_kind()
    #
    #


    def  tearDown(self):
        print("function teardown")
        MWiki.delete(self.uid)
