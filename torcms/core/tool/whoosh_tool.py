# -*- coding:utf-8 -*-

from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import And, Term

def singleton(cls, *args, **kwargs):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


@singleton
class YunSearch():
    '''
    For searching in whoosh database.
    '''
    def __init__(self):
        self.whbase = open_dir("database/whoosh")
        self.parser = QueryParser("content", schema=self.whbase.schema)

    def get_all_num(self, keyword, catid=''):
        queryit = self.parser.parse(keyword)
        if catid == '':
            pass
        else:
            queryit = And([Term("catid", catid), queryit])

        return len(self.whbase.searcher().search(queryit).docs())

    def search(self, keyword, limit=20):
        queryit = self.parser.parse(keyword)
        try:
            queryres = self.whbase.searcher().search(queryit, limit=limit)
            return queryres
        finally:
            pass

    def search_pager(self, keyword, catid='', page_index=1, doc_per_page=10):

        queryit = self.parser.parse(keyword)
        if catid == '':
            pass
        else:
            queryit = And([Term("catid", catid), queryit])
        try:
            queryres = self.whbase.searcher().search(queryit, limit=page_index * doc_per_page)
            return queryres[(page_index - 1) * doc_per_page: page_index * doc_per_page]
        finally:
            pass
