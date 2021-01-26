# -*- coding:utf-8 -*-
from torcms.core import tools
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
from torcms.model.usage_model import MUsage


class TestMUsage():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')

        self.postid = '12345'
        self.userid = ''
        self.uid = ''
        self.tag_id = '87hy'
        self.slug = 'qwqqq'
        self.postid2 = 'qqqew'
        self.uu = MPost()

    def add_message(self, **kwargs):
        post_data = {
            'name': kwargs.get('name', 'category'),
            'slug': kwargs.get('slug', self.slug),
            'order': kwargs.get('order', '0'),
            'kind': kwargs.get('kind1', '1'),
            'pid': kwargs.get('pid', '0000'),
        }
        MCategory.add_or_update(self.tag_id, post_data)

        p_d = {
            'title': kwargs.get('title', 'iiiii'),
            'cnt_md': kwargs.get('cnt_md', 'grgr'),
            'time_create': kwargs.get('time_create', '1992'),
            'time_update': kwargs.get('time_update', '1996070600'),
            'user_name': kwargs.get('user_name', 'yuanyuan'),
            'view_count': kwargs.get('view_count', 1),
            'logo': kwargs.get('logo', 'prprprprpr'),
            'memo': kwargs.get('memo', ''),
            'order': kwargs.get('order', '1'),
            'keywords': kwargs.get('keywords', ''),
            'extinfo': kwargs.get('extinfo', {}),
            'kind': kwargs.get('kind2', '1'),
            'valid': kwargs.get('valid', 1),

        }
        post_id = kwargs.get('post_id', self.postid)

        MPost.create_post(post_id, p_d)

        MPost2Catalog.add_record(self.postid, self.tag_id)

    def add_usage(self, **kwargs):
        id = kwargs.get('post_id', self.postid)
        MUsage.add_or_update(self.userid, id, '1')
        aa = MUsage.query_by_post(id)
        print('add_usage')
        print(aa)

        for i in aa:
            if i.user_id == self.userid:
                self.uid = i.uid
        print(self.uid)

    def test_query_by_post(self):
        self.add_message()
        self.add_usage()
        aa = MUsage.query_by_post(self.postid)
        tf = False
        for i in aa:
            if i.user_id == self.userid:
                assert i.uid == self.uid
                tf = True
                break
        self.tearDown()
        assert tf

    #
    # def test_get_all(self):
    #     self.tearDown()
    #     aa = MUsage.get_all()
    #     print(aa.count())
    #     self.add_message()
    #     self.add_usage()
    #     aa =MUsage.get_all()
    #     print('gggggggggggggggggggggggggg')
    #     print(aa)
    #     print(aa.count())
    #     tf = False
    #     for i in aa:
    #         print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
    #         print(i)
    #         if i.post_id == self.postid:
    #             assert i.uid == self.uid
    #             tf = True
    #             break
    #     # self.tearDown()
    #     assert tf

    def test_query_random(self):
        self.tearDown()
        self.add_message()
        self.add_usage()
        aa = MUsage.query_random(limit=300)
        tf = False
        for i in aa:
            if i.post_id == self.postid:
                assert i.uid == self.uid
                tf = True
                break
        self.tearDown()
        assert tf

    def test_query_recent(self):
        self.add_message()
        self.add_usage()
        aa = MUsage.query_recent(self.userid, '1', num=300)
        tf = False
        for i in aa:
            if i.post_id == self.postid:
                assert i.uid == self.uid
                tf = True
                break
        self.tearDown()
        assert tf

    def test_query_recent_by_cat(self):
        self.add_message()
        self.add_usage()
        aa = MUsage.query_recent_by_cat(self.userid, self.tag_id, 8)
        tf = False
        for i in aa:
            if i.post_id == self.postid:
                assert i.uid == self.uid
                tf = True
                break
        self.tearDown()
        assert tf

    def test_query_most(self):
        self.add_message()
        self.add_usage()
        aa = MUsage.query_most(self.userid, '1', 8)
        tf = False
        for i in aa:
            if i.post_id == self.postid:
                assert i.uid == self.uid
                tf = True
                break
        self.tearDown()
        assert tf

    def test_query_by_signature(self):

        self.add_message()
        self.add_usage()
        aa = MUsage.query_by_signature(self.userid, self.postid)
        assert aa[0].uid == self.uid

        self.tearDown()

    def test_count_increate(self):
        self.add_message()
        self.add_usage()
        MUsage.count_increate(self.uid, self.tag_id, 8)
        aa = MUsage.query_recent(self.userid, '1')
        tf = False
        for i in aa:
            if i.user_id == self.userid:
                assert i.count >= 8
                tf = True
                break
        self.tearDown()
        assert tf

    def test_add_or_update(self):
        self.add_message()
        self.add_usage()
        aa = MUsage.query_recent(self.userid, '1')
        tf = False
        for i in aa:
            if i.user_id == self.userid:
                self.uid = i.uid
                assert i.post_id == self.postid
                tf = True
                break
        self.tearDown()
        assert tf

    def tearDown(self):
        print("function teardown")

        MCategory.delete(self.tag_id)

        MPost.delete(self.postid)

        MPost2Catalog.remove_relation(self.postid, self.tag_id)
