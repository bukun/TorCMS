'''
Running whoosh script.
'''

import os

import html2text
import tornado.escape
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import ID, TEXT, Schema
from whoosh.index import create_in, open_dir

from config import SITE_CFG, kind_arr, post_type, router_post
from torcms.model.post_model import MPost
from torcms.model.wiki_model import MWiki

try:
    from jieba.analyse import ChineseAnalyzer
except Exception as err:
    print(repr(err))
    ChineseAnalyzer = None

SITE_CFG['LANG'] = SITE_CFG.get('LANG', 'zh')
WHOOSH_BASE = 'database/whoosh'

# Using jieba lib for Chinese.
if SITE_CFG['LANG'] == 'zh' and ChineseAnalyzer:
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


# def do_for_post(rand=True, _=''):
#     if rand:
#         recs = MPost.query_random(num=10, kind='1')
#     else:
#         recs = MPost.query_recent(num=2, kind='1')
#
#     for rec in recs:
#         text2 = rec.title + ',' + html2text.html2text(
#             tornado.escape.xhtml_unescape(rec.cnt_html))
#         writer.update_document(
#             title=rec.title,
#             catid='sid1',
#             type=post_type['1'],
#             link='/post/{0}'.format(rec.uid),
#             content=text2,
#         )
#         writer.commit()


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
