# coding: utf-8

import os
from whoosh.qparser import QueryParser
from whoosh.index import  open_dir


def query_wh(whoosh_db):
    new_list = []
    index = open_dir(whoosh_db)  # 读取建立好的索引
    with index.searcher():
        parser = QueryParser("content", index.schema)
        myquery = parser.parse("思想")


        queryres = index.searcher().search(myquery, limit=20)

        for result1 in queryres:
            # print("*" * 50)
            # print(dict(result1))
            # print("*" * 50)
            new_list.append(dict(result1))
    print("-" * 50)
    print(new_list)
    print("*" * 50)