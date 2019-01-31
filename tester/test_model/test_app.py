# -*- coding:utf-8 -*-

'''
Testing for map app.
'''

from torcms.core import tools
from torcms.model.post_model import MPost


class TestApp():
    '''
    Testing for map app.
    '''

    def setup(self):
        print('setup 方法执行于本类中每条用例之前')

        self.title = '哈哈sdfsdf'
        self.uid = 'g' + tools.get_uu4d()

    def test_insert(self):
        uid = self.uid
        post_data = {
            'title': self.title,
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'extinfo': '',
            'valid': 1,
            'kind': '1',
        }
        extinfo = {}

        MPost.add_meta(uid, post_data, extinfo)
        tt = MPost.get_by_uid(uid)
        assert tt.uid == uid

    def test_insert2(self):
        uid = self.uid
        post_data = {

            'title': '',
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '9',
            'extinfo': ''
        }
        extinfo = {}

        MPost.add_meta(uid, post_data, extinfo)
        tt = MPost.get_by_uid(uid)
        assert tt == None

        post_data = {
            'title': '1',
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '9',
            'extinfo': ''
        }
        uu = MPost.add_meta(self.uid, post_data)
        assert uu == False

        post_data = {
            'title': '天',
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '2',
            'extinfo': ''
        }
        uu = MPost.add_meta(self.uid, post_data)
        assert uu == False

        post_data = {
            'title': self.title,
            'keywords': 'sd,as',
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'logo': '/static/',
            'user_name': 'ss',
            'kind': '2',
            'extinfo': ''
        }
        uu = MPost.add_meta(self.uid, post_data)
        tt = MPost.get_by_uid(uid)
        assert tt.uid == uu

    def test_query_random(self):
        MPost.query_random()
        assert True

    def test_query_recent(self):
        MPost.query_recent()
        assert True

    def test_query_all(self):
        MPost.query_all()
        assert True

    def test_query_keywords_empty(self):
        MPost.query_keywords_empty()
        assert True

    def test_query_recent_edited(self):
        MPost.query_recent_edited(1539069122)
        assert True

    def test_query_dated(self):
        MPost.query_dated()
        assert True

    def test_query_most_pic(self):
        MPost.query_most_pic(8)
        assert True

    def test_get_all(self):
        MPost.get_all()
        assert True

    def test_modify_init(self):
        post_data = {
            'kind': '2',
            'keywords': 'key',
        }
        MPost.modify_init(self.uid, post_data)
        assert True

    def test_get_view_count(self):
        MPost.get_view_count(self.uid)
        assert True

    def tearDown(self):
        print("function teardown")
        tt = MPost.get_by_uid(self.uid)
        if tt:
            MPost.delete(tt.uid)
