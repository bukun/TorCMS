# coding: utf-8

import os

from whoosh.analysis import StemmingAnalyzer
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from config import SITE_CFG
from query_whoosh1 import *

def create_wh(title, url, content):
    try:
        from jieba.analyse import ChineseAnalyzer
    except:
        ChineseAnalyzer = None

    SITE_CFG['LANG'] = SITE_CFG.get('LANG', 'zh')

    # Using jieba lib for Chinese.
    if SITE_CFG['LANG'] == 'zh' and ChineseAnalyzer:
        schema = Schema(title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                        id=TEXT(stored=True),
                        link=ID(unique=True, stored=True),
                        content=TEXT(stored=True, analyzer=ChineseAnalyzer()))
    else:
        schema = Schema(title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
                        id=TEXT(stored=True),
                        link=ID(unique=True, stored=True),
                        content=TEXT(stored=True, analyzer=StemmingAnalyzer()))
    whoosh_db = 'database/whoosh1'
    if os.path.exists(whoosh_db):
        create_idx = open_dir(whoosh_db)
    else:
        os.makedirs(whoosh_db)
        create_idx = create_in(whoosh_db, schema)

    writer = create_idx.writer()

    writer.update_document(
        title=title,
        link=url,
        content=content
    )

    print("建立完成一个索引")
    writer.commit()
    # 以上为建立索引的过程
    query_wh(whoosh_db)
