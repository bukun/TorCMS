# -*- coding:utf-8 -*-
from torcms.core import tools
from torcms.model.user_model import MUser
from torcms.model.wiki_hist_model import MWikiHist
from torcms.model.wiki_model import MWiki


class TestMWikiHist():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.wiki_uid = ''
        self.username = 'snow'
        self.title = 'bibo'
        self.uid = ''
        self.user_uid = ''

    def add_wiki(self):
        p_d = {
            'title': self.title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': self.username,

        }
        MWiki.create_wiki(p_d)
        aa = MWiki.get_by_wiki(self.title)
        self.wiki_uid = aa.uid

    def add_user(self, **kwargs):
        name = kwargs.get('user_name', self.username)
        post_data = {
            'user_name': name,
            'user_pass': kwargs.get('user_pass', 'g131322'),
            'user_email': kwargs.get('user_email', 'name@kljhqq.com'),
        }

        MUser.create_user(post_data)
        aa = MUser.get_by_name(name)
        self.user_uid = aa.uid

    def add_w_h(self):
        self.add_user()
        self.add_wiki()
        post_data = MWiki.get_by_uid(self.wiki_uid)
        userinfo = MUser.get_by_uid(self.user_uid)
        aa = MWikiHist.create_wiki_history(post_data, userinfo)
        self.uid = aa

    def test_get_last(self):
        self.add_w_h()
        aa = MWikiHist.get_last(self.wiki_uid)
        assert aa.uid == self.uid
        self.tearDown()

    def test_get_by_uid(self):
        self.add_w_h()
        aa = MWikiHist.get_by_uid(self.uid)
        assert aa.user_name == self.username
        self.tearDown()

    def test_update_cnt(self):
        self.add_w_h()
        aa = MWikiHist.get_by_uid(self.uid)
        post_data = {
            'user_name': self.username,
            'cnt_md': 'asdf'
        }
        MWikiHist.update_cnt(self.uid, post_data)
        bb = MWikiHist.get_by_uid(self.uid)
        assert aa.cnt_md != bb.cnt_md
        assert bb.cnt_md == post_data['cnt_md']
        self.tearDown()

    def test_query_by_wikiid(self):
        self.add_w_h()
        aa = MWikiHist.query_by_wikiid(self.wiki_uid)
        tf = False
        for i in aa:
            if i.uid == self.uid:
                tf = True
                break
        self.tearDown()
        assert tf

    def test_create_wiki_history(self):
        self.add_w_h()
        self.tearDown()

    def test_delete(self):
        self.add_w_h()
        assert self.uid != ''
        aa = MWikiHist.delete(self.uid)
        assert aa
        self.tearDown()

    def tearDown(self):
        print("function teardown")
        MUser.delete(self.user_uid)
        MWiki.delete(self.wiki_uid)
        MWikiHist.delete(self.uid)
