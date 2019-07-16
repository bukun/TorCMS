# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.label_model import MLabel
from torcms.model.label_model import MPost2Label


class TestLabel():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.uu = MLabel()
        self.name = 'name'
        self.tmpl_uid = ''
        self.uid = tools.get_uu4d()

    def test_create_tag(self):
        post_data = {
            'name': 'titlesdf',
        }
        newid = MLabel.create_tag(post_data['name'])

        tt = MLabel.get_id_by_name(post_data['name'])
        # assert tt.uid == suid
        self.tmpl_uid = tt
        assert tt == newid

    def test_create_tag_2(self):
        '''Wiki insert: Test invalid title'''
        post_data = {
            'name': self.name,
        }
        uu = self.uu.create_tag(post_data['name'])
        # assert uu == False

        post_data = {
            'name': '',
        }
        uu = self.uu.create_tag(post_data['name'])
        # assert uu == False

    def test_create_tag_with_uid(self):
        '''Wiki insert: Test invalid title'''
        post_data = {
            'name': self.name,
        }

        self.uu.create_tag_with_uid(self.uid, post_data['name'])
        assert True

    def test_get_id_by_name(self):
        MLabel.get_id_by_name(self.name)
        assert True

    def test_get_by_slug(self):
        MLabel.get_by_slug(self.name)
        assert True

    def test_delete(self):
        MLabel.delete(self.uid)
        assert True

    def tearDown(self):
        print("function teardown")
        tt = self.uu.get_id_by_name(self.name)
        self.uu.delete(self.tmpl_uid)


class TestMPost2Label():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')

        self.name = 'name'
        self.tmpl_uid = ''
        self.uid = tools.get_uu4d()
        self.post_id = '11111'
        self.tag_id = '11111'

    def test_query_count(self):
        MPost2Label.query_count(self.uid)
        assert True

    def test_remove_relation(self):
        MPost2Label.remove_relation(self.post_id, self.tag_id)
        assert True

    def test_generate_catalog_list(self):
        MPost2Label.generate_catalog_list(self.uid)
        assert True

    def test_get_by_uid(self):
        MPost2Label.get_by_uid(self.post_id)
        assert True

    def test_get_by_info(self):
        MPost2Label.get_by_info(self.post_id, self.tag_id)
        assert True

    def test_add_record(self):
        MPost2Label.add_record(self.post_id, self.name)
        assert True

    def test_total_number(self):
        MPost2Label.total_number(self.name)
        assert True

    def test_query_pager_by_slug(self):
        MPost2Label.query_pager_by_slug(self.name)
        assert True
