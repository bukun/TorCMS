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
        results = self.whbase.searcher().search(queryit)
        deduped_results = list(dedupe(results, key=lambda s: s['content']))
        return len(deduped_results)

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

            deduped_queryres = list(dedupe(queryres, key=lambda s: s['content']))

            return deduped_queryres[(page_index - 1) * doc_per_page: page_index * doc_per_page]
        finally:
            pass


def dedupe(items, key=None):
    """
    items: 哈希或者不可哈希的序列
    key: 若items为不可哈希的序列(dict等)则需要指定一个函数
    """
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)
