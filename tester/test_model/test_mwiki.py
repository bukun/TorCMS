# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.wiki_model import MWiki
import tornado.escape


class TestWiki():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uu = MWiki()
        self.raw_count = self.uu.get_counts()
        self.wiki_title = 'lkablkjcdefg'

    def test_insert(self):
        raw_count = self.uu.get_counts()
        post_data = {
            'title': self.wiki_title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
        }
        if self.uu.insert_data(post_data):
            new_count = self.uu.get_counts()

            tt = self.uu.get_by_wiki(self.wiki_title)

            assert tt.title == post_data['title']
            assert tt.cnt_md == tornado.escape.xhtml_unescape(post_data['cnt_md'])
            assert raw_count + 1 == new_count

    def test_insert_2(self):
        '''Wiki insert: Test invalid title'''
        post_data = {
            'title': '',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
        }
        uu = self.uu.insert_data(post_data)
        assert uu == False

        post_data = {
            'title': '1',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
        }
        uu = self.uu.insert_data(post_data)
        assert uu == False

        post_data = {
            'title': '天',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
        }
        uu = self.uu.insert_data(post_data)
        assert uu == False

    def test_get_by_title(self):
        post_data = {
            'title': self.wiki_title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
        }
        uid = self.uu.insert_data(post_data)

        ss = self.uu.get_by_uid(uid)
        assert ss.title == post_data['title']

        tt = self.uu.get_by_title(self.wiki_title)
        assert tt.title == post_data['title']

    def test_get_by_title2(self):
        '''Test Wiki title with SPACE'''
        post_data = {
            'title': '  ' + self.wiki_title + '  ',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
        }
        uid = self.uu.insert_data(post_data)

        ss = self.uu.get_by_uid(uid)
        assert ss.title == self.wiki_title

        tt = self.uu.get_by_title(self.wiki_title)
        assert tt.title == post_data['title'].strip()

    def test_upate_by_view_count(self):

        post_data = {

            'title': self.wiki_title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
        }
        if self.uu.insert_data(post_data):

            rec = self.uu.get_by_wiki(self.wiki_title)

            viewcount0 = rec.view_count
            assert viewcount0 == 2
            for x in range(100):
                self.uu.update_view_count_by_uid(rec.uid)

            viewcount1 = self.uu.get_by_wiki(self.wiki_title).view_count
            assert viewcount1 == 103

    def test_upate(self):
        assert True

    def tearDown(self):
        print ("function teardown")
        tt = self.uu.get_by_wiki(self.wiki_title)
        if tt:
            self.uu.delete(tt.uid)
