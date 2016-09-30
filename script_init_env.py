# -*- coding:utf-8 -*-

import os
import html2text
import tornado.escape
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
from torcms.model.post_model import MPost
from torcms.model.info_model import MInfor

whoosh_database = 'database/whoosh'

def build_whoosh_database():
    analyzer = ChineseAnalyzer()
    schema = Schema(title=TEXT(stored=True, analyzer=analyzer), type=TEXT(stored=True), link=ID(stored=True),
                    content=TEXT(stored=True, analyzer=analyzer))
    ix = create_in(whoosh_database, schema)

    writer = ix.writer()

    uu = MInfor()

    tt = uu.get_all()
    for rec in tt:
        text2 = html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
        writer.add_document(
             title=rec.title,
             type='<span style="color:red;">[信息]</span>',
             link='/info/{0}'.format(rec.uid),
             content= text2,
        )

    mpost = MPost()
    recs = mpost.query_all()
    for rec in recs:
        text2 = html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
        print(text2)
        writer.add_document(
            title=rec.title,
            type='<span style="color:blue;">[文档]</span>',
            link='/post/{0}.html'.format(rec.uid),
            content=text2
        )

    writer.commit()

if __name__ == '__main__':
    build_whoosh_database()

