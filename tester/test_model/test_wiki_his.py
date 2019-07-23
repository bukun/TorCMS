# -*- coding:utf-8 -*-
from torcms.model.wiki_hist_model import MWikiHist
from torcms.core import tools


def Test():
    assert MWikiHist()


class TestMWikiHist():
    def setup(self):
        print('setup 方法执行于本类中每条用例之前')

        self.postid = '12345'

        self.uid = tools.get_uuid()

    def test_get_last(self):
        MWikiHist.get_last(self.postid)
        assert True

    def test_get_by_uid(self):
        MWikiHist.get_by_uid(self.uid)
        assert True

    def test_update_cnt(self):
        post_data = {
            'user_name': 'giser',
            'cnt_md': 'asdf'
        }
        MWikiHist.update_cnt(self.uid, post_data)
        assert True

    def test_query_by_wikiid(self):
        MWikiHist.query_by_wikiid(self.uid)
        assert True

    # def test_create_wiki_history(self):
    #     post_data = MWikiHist.get_by_uid(self.uid)
    #     MWikiHist.create_wiki_history(post_data)
    #     assert True

    def test_delete(self):
        MWikiHist.delete(self.uid)
        assert True
