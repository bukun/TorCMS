# -*- coding: UTF-8 -*-

import os
import html2text
import tornado.escape

from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from jieba.analyse import ChineseAnalyzer
from torcms.model.post_model import MPost
# from torcms.model.info_model import MInfor
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.wiki_model import MWiki
from config import router_post, kind_arr, post_type


def do_for_app(writer, rand=True, kind='', doc_type=None):
    '''
    生成whoosh，根据配置文件中类别。
    :param writer:
    :param rand:
    :param kind:
    :param doc_type:
    :return:
    '''
    if doc_type is None:
        doc_type = {}
    if rand:
        recs = MPost.query_random(num=10, kind=kind)
    else:
        recs = MPost.query_recent(num=2, kind=kind)

    for rec in recs:
        text2 = rec.title + ',' + html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
        writer.update_document(
            catid='sid' + kind,
            title=rec.title,
            type=doc_type[rec.kind],
            link='/{0}/{1}'.format(router_post[rec.kind], rec.uid),
            content=text2
        )


# def do_for_app2(writer, rand=True):
#     '''
#     生成whoosh，根据数据库中类别。
#     :param writer:
#     :param rand:
#     :return:
#     '''
#     if rand:
#         recs = MPost.query_random(num = 10, kind = '2')
#     else:
#         recs = MPost.query_recent(2)
#
#     for rec in recs:
#         text2 = rec.title + ',' + html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
#
#         info = MPost2Catalog.get_entry_catalog(rec.uid)
#         if info:
#             pass
#         else:
#             continue
#
#         catid = info.tag.uid[:2] + '00'
#
#         cat_name = ''
#         if 'def_cat_uid' in rec.extinfo and rec.extinfo['def_cat_uid']:
#             taginfo = MCategory.get_by_uid(rec.extinfo['def_cat_uid'][:2] + '00')
#             if taginfo:
#                 cat_name = taginfo.name
#         writer.update_document(
#             title=rec.title,
#             catid=catid,
#             type='<span style="color:red;">[{0}]</span>'.format(cat_name),
#             link='/{0}/{1}'.format(router_post[rec.kind], rec.uid),
#             content=text2
#         )


def do_for_post(writer, rand=True, doc_type=''):
    if rand:
        recs = MPost.query_random(num=10, kind='1')
    else:
        recs = MPost.query_recent(num=2, kind='1')

    for rec in recs:
        text2 = rec.title + ',' + html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
        writer.update_document(
            title=rec.title,
            catid='sid1',
            type=doc_type,
            link='/post/{0}'.format(rec.uid),
            content=text2
        )


def do_for_wiki(writer, rand=True, doc_type=''):
    if rand:
        recs = MWiki.query_random(num=10, kind='1')
    else:
        recs = MWiki.query_recent(num=2, kind='1')

    for rec in recs:
        text2 = rec.title + ',' + html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
        writer.update_document(
            title=rec.title,
            catid='sid1',
            type=doc_type,
            link='/wiki/{0}'.format(rec.title),
            content=text2
        )


def do_for_page(writer, rand=True, doc_type=''):
    if rand:
        recs = MWiki.query_random(num=4, kind='2')
    else:
        recs = MWiki.query_recent(num=2, kind='2')

    for rec in recs:
        text2 = rec.title + ',' + html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
        writer.update_document(
            title=rec.title,
            catid='sid1',
            type=doc_type,
            link='/page/{0}'.format(rec.uid),
            content=text2
        )


def gen_whoosh_database(kind_arr=None, post_type=None):
    '''
    kind_arr, define the `type` except Post, Page, Wiki
    post_type, define the templates for different kind.
    :param if_rand:
    :param kind_arr:
    :param post_type:
    :return:
    '''
    if kind_arr is None:
        kind_arr = []
    if post_type is None:
        post_type = {}
    analyzer = ChineseAnalyzer()
    schema = Schema(title=TEXT(stored=True, analyzer=analyzer),
                    catid=TEXT(stored=True),
                    type=TEXT(stored=True),
                    link=ID(unique=True, stored=True),
                    content=TEXT(stored=True, analyzer=analyzer))
    whoosh_db = 'database/whoosh'
    if not os.path.exists(whoosh_db):
        os.makedirs(whoosh_db)
        create_idx = create_in(whoosh_db, schema)
    else:
        create_idx = open_dir(whoosh_db)

    writer = create_idx.writer()

    # do_for_app2(writer, rand=if_rand)

    for switch in [True, False]:
        do_for_post(writer, rand=switch, doc_type=post_type['1'])
        do_for_wiki(writer, rand=switch, doc_type=post_type['1'])
        do_for_page(writer, rand=switch, doc_type=post_type['1'])

        for kind in kind_arr:
            do_for_app(writer, rand=switch, kind=kind, doc_type=post_type)
    writer.commit()


def run():
    gen_whoosh_database(kind_arr=kind_arr, post_type=post_type)
