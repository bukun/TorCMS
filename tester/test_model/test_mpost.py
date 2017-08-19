# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.post_model import MPost
import tornado.escape


class TestPost():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uu = MPost()
        self.raw_count = self.uu.get_counts()
        self.post_title = 'ccc'
        self.uid = tools.get_uu4d()

    def test_insert(self):
        raw_count = self.uu.get_counts()

        post_data = {
            'title': self.post_title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',

        }
        self.uu.create_post(self.uid, post_data)
        new_count = self.uu.get_counts()

        tt = self.uu.get_by_uid(self.uid)

        assert tt.title == post_data['title']
        assert tt.cnt_md == tornado.escape.xhtml_unescape(post_data['cnt_md'])
        assert tt.cnt_html == tools.markdown2html(post_data['cnt_md'])
        assert raw_count + 1 == new_count

    def test_insert_2(self):
        '''Wiki insert: Test invalid title'''

        post_data = {
            'title': '',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        uu = self.uu.create_post(self.uid, post_data)
        assert uu == False

        post_data = {
            'title': '1',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        uu = self.uu.create_post(self.uid, post_data)
        assert uu == False

        post_data = {
            'title': '天',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        uu = self.uu.create_post(self.uid, post_data)
        assert uu == False

    def test_get_by_title(self):

        post_data = {

            'title': self.post_title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        uid = self.uu.create_post(self.uid, post_data)

        ss = self.uu.get_by_uid(uid)
        assert ss.title == post_data['title']

    def test_get_by_title2(self):

        '''Test Wiki title with SPACE'''

        post_data = {

            'title': '  ' + self.post_title + '  ',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        uid = self.uu.create_post(self.uid, post_data)

        ss = self.uu.get_by_uid(uid)
        assert ss.title == self.post_title

    def test_update_by_uid(self):
        uid = self.uid
        post_data = {
            'title': 'a123sdf',
            'cnt_md': '1212sadf',
            'user_name': 'asdf',
            'logo': 'asqwef',
            'keywords': 'aseef',
        }
        self.uu.create_post(uid, post_data)
        new_count = self.uu.get_counts()

        # assert self.raw_count + 1 == new_count

        post_data2 = {

            'title': 'a123sdf',
            'cnt_md': '1212sadf',
            'user_name': 'asdf',
            'logo': '1111asqwef',
            'keywords': '111aseef',
        }

        self.uu.update(uid, post_data2)

        new_count = self.uu.get_counts()

        # assert self.raw_count + 1 == new_count

        tt = self.uu.get_by_uid(uid)

        # assert tt.title != post_data['title'][0]
        # assert tt.cnt_md != post_data['cnt_md'][0]
        # assert tt.user_name != int(post_data['user_name'][0])
        # assert tt.logo != post_data['logo'][0]
        # assert tt.keywords != post_data['keywords'][0]

    #
    # assert tt.title == post_data['title'][0]
    # assert tt.cnt_md == post_data['cnt_md'][0]
    # assert tt.user_name == int(post_data['user_name'][0])
    # assert tt.logo == post_data['logo'][0]
    # assert tt.keywords == post_data['keywords'][0]

    def test_query_cat_random(self):
        self.uu.query_cat_random('')
        assert True

    def test_query_recent(self):
        self.uu.query_recent()
        assert True

    def test_query_all(self):
        self.uu.query_all()
        assert True

    def test_query_keywords_empty(self):
        self.uu.query_keywords_empty()
        assert True

    def test_query_dated(self):
        self.uu.query_dated()
        assert True

    def test_query_most_pic(self):
        self.uu.query_most_pic(3)
        assert True

    def test_query_cat_recent(self):
        self.uu.query_cat_recent(3, 3)
        assert True

    def test_query_most(self):
        self.uu.query_most()
        assert True

    def test_update_keywords(self):
        self.uu.update_misc(self.uid, keywords='adf')
        assert True

    def test_update_view_count_by_uid(self):
        uid = tools.get_uu4d()
        post_data = {

            'title': self.post_title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
        }
        self.uu.create_post(uid, post_data)

        rec = self.uu.get_by_uid(uid)

        viewcount0 = rec.view_count
        assert viewcount0 == 1
        for x in range(100):
            self.uu.update_misc(rec.uid, count=True)

        viewcount1 = self.uu.get_by_uid(uid).view_count

        assert viewcount1 == 101

    def test_upate(self):
        assert True

    def tearDown(self):
        print("function teardown")
        tt = self.uu.get_by_uid(self.uid)
        if tt:
            self.uu.delete(tt.uid)
