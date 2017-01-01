# -*- coding:utf-8 -*-

from whoosh.index import open_dir
# from jieba.analyse import ChineseAnalyzer
from whoosh.qparser import QueryParser
from whoosh.query import *

# analyzer = ChineseAnalyzer()
def singleton(cls, *args, **kwargs):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton
@singleton
class yunsearch():
    def __init__(self):
        self.ix = open_dir("database/whoosh")
        self.parser = QueryParser("content", schema=self.ix.schema)

    def get_all_num(self, keyword, catid=''):
        q = self.parser.parse(keyword)
        if catid == '':
            pass
        else:
            q = And([Term("catid", catid), q])
        return len(self.ix.searcher().search(q).docs())

    def search(self, keyword, limit=20):
        q = self.parser.parse(keyword)
        try:
            tt = self.ix.searcher().search(q, limit=limit)
            return (tt)
        finally:
            pass

    def search_pager(self, keyword, catid='', page_index=1, doc_per_page=10):

        q = self.parser.parse(keyword)
        if catid == '':
            pass
        else:
            q = And([Term("catid", catid), q])
        try:
            tt = self.ix.searcher().search(q, limit=page_index * doc_per_page)
            return (tt[(page_index - 1) * doc_per_page: page_index * doc_per_page])
        finally:
            pass

