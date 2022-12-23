# -*- coding:utf-8 -*-

import os
import html2text
import tornado.escape

from whoosh.qparser import QueryParser
from whoosh.query import And, Term
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import ID, TEXT, Schema
from whoosh.index import create_in, open_dir

from torcms.model.post_model import MPost
from torcms.model.wiki_model import MWiki
from config import post_type, router_post, kind_arr, SITE_CFG

try:
    from jieba.analyse import ChineseAnalyzer
except Exception as err:
    print(repr(err))
    ChineseAnalyzer = None

WHOOSH_BASE = 'database/whoosh'

# Using jieba lib for Chinese.
if SITE_CFG.get('LANG', 'zh') == 'zh' and ChineseAnalyzer:
    TOR_SCHEMA = Schema(title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                        catid=TEXT(stored=True),
                        type=TEXT(stored=True),
                        link=ID(unique=True, stored=True),
                        content=TEXT(stored=True, analyzer=ChineseAnalyzer()))
else:
    TOR_SCHEMA = Schema(title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
                        catid=TEXT(stored=True),
                        type=TEXT(stored=True),
                        link=ID(unique=True, stored=True),
                        content=TEXT(stored=True, analyzer=StemmingAnalyzer()))

if os.path.exists(WHOOSH_BASE):
    TOR_IDX = open_dir(WHOOSH_BASE)
else:
    os.makedirs(WHOOSH_BASE)
    TOR_IDX = create_in(WHOOSH_BASE, TOR_SCHEMA)


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
        return len(results)
        # return len(self.whbase.searcher().search(queryit).docs())

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
            queryres = self.whbase.searcher().search(queryit,
                                                     limit=page_index *
                                                           doc_per_page)
            return queryres[(page_index - 1) * doc_per_page:page_index *
                                                            doc_per_page]
        finally:
            pass


def do_for_document(rand=True, kind='', _=None):
    '''
    生成whoosh，根据配置文件中类别。
    '''

    if rand:
        recs = MPost.query_random(num=10, kind=kind)
    else:
        recs = MPost.query_recent(num=2, kind=kind)

    for rec in recs:
        text2 = rec.title + ',' + html2text.html2text(
            tornado.escape.xhtml_unescape(rec.cnt_html))

        writer = TOR_IDX.writer()
        writer.update_document(catid='sid' + kind,
                               title=rec.title,
                               type=post_type[rec.kind],
                               link='/{0}/{1}'.format(router_post[rec.kind],
                                                      rec.uid),
                               content=text2)
        writer.commit()


def do_for_wiki(rand=True, _=''):
    if rand:
        recs = MWiki.query_random(num=10, kind='1')
    else:
        recs = MWiki.query_recent(num=2, kind='1')

    for rec in recs:
        text2 = rec.title + ',' + html2text.html2text(
            tornado.escape.xhtml_unescape(rec.cnt_html))

        writer = TOR_IDX.writer()
        writer.update_document(title=rec.title,
                               catid='sid1',
                               type=post_type['1'],
                               link='/wiki/{0}'.format(rec.title),
                               content=text2)
        writer.commit()


def do_for_page(rand=True, _=''):
    if rand:
        recs = MWiki.query_random(num=4, kind='2')
    else:
        recs = MWiki.query_recent(num=2, kind='2')

    for rec in recs:
        text2 = rec.title + ',' + html2text.html2text(
            tornado.escape.xhtml_unescape(rec.cnt_html))

        writer = TOR_IDX.writer()
        writer.update_document(title=rec.title,
                               catid='sid1',
                               type=post_type['1'],
                               link='/page/{0}'.format(rec.uid),
                               content=text2)
        writer.commit()


def gen_whoosh_database(kind_arr):
    '''
    kind_arr, define the `type` except Post, Page, Wiki
    post_type, define the templates for different kind.
    '''
    for switch in [True, False]:
        # do_for_post(rand=switch)
        do_for_document(rand=switch, kind='1')
        do_for_wiki(rand=switch)
        do_for_page(rand=switch)
        for kind in kind_arr:
            do_for_document(rand=switch, kind=kind)


def run():
    '''
    Run it.
    '''
    gen_whoosh_database(kind_arr=kind_arr)
