# -*- coding:utf-8 -*-
import time

import tornado.escape

from torcms.core import tools
from torcms.model.category_model import MCategory
from torcms.model.label_model import MLabel, MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
from torcms.model.process_model import MProcess

from faker import Faker

class TestMProcess():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.mpost = MPost()
        self.m2c = MPost2Catalog()
        self.ml = MLabel()
        self.m2l = MPost2Label()
        self.labeluid = '9999'
        self.raw_count = self.mpost.get_counts()
        self.post_title = 'ccc'
        self.uid = tools.get_uu4d()
        self.post_id = '66565'
        self.tag_id = '2342'
        self.post_id2 = '89898'
        self.slug = 'huio'
        self.insert()
        self.mprocess = MProcess()
        self.fake = Faker(locale="zh_CN")
    def tearDown(self, process_id = ''):
        print("function teardown")

        self.mpost.delete(self.uid)
        MCategory.delete(self.tag_id)
        self.mpost.delete(self.post_id2)
        self.mpost.delete(self.post_id)

        if process_id:
            self.mprocess.delete_by_uid(process_id)

        MPost2Catalog.remove_relation(self.post_id, self.tag_id)
        tt = MLabel.get_by_slug(self.slug)
        if tt:
            MLabel.delete(tt.uid)

    def insert(self):

        post_data = {
            'title': self.post_title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',

        }
        self.mpost.add_or_update(self.uid, post_data)


    def test_insert_2(self):
        '''Wiki insert: Test invalid title'''
        tt = self.mprocess.create(self.uid)

        self.tearDown(tt)
        print(tt)
        assert tt
