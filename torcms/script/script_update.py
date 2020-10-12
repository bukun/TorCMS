'''
用 SQLite 中的访问日志，更新PostgreSQL.
数据量大的时候比较慢，
按脚本运行。

简单的方法，使用下面的语句更新，但是数据量大的时候很慢。更改为逐条更新：

    UPDATE tabpost SET access_1d=(SELECT count(*) FROM
        tabaccess WHERE (tabaccess.post_id = tabpost.uid)
        and (tabaccess.uid >= {}));'.format(ts1d)
'''

import time
import sqlite3

from .script_sitemap import run_sitemap, run_editmap
from config import DB_CON

CONN = sqlite3.connect('./database/log_access.db')
CUR = CONN.cursor()


def ts_helper():
    timestamp = int(time.time())
    ts1d = timestamp - 24 * 60 * 60
    ts7d = timestamp - 7 * 24 * 60 * 60
    ts30d = timestamp - 30 * 24 * 60 * 60
    return (ts1d, ts7d, ts30d)


def echo_info():

    cur = DB_CON.cursor()
    print('访问总数目：')
    CUR.execute('SELECT count(*) FROM tabaccess')
    recs = CUR.fetchall()
    for rec in recs:
        print(rec)

    print('访问总数目：')
    cur.execute('select count(*) from tabpost')
    recs = cur.fetchall()
    for rec in recs:
        print(rec)

    print('近24小时：')
    recent_1d = '''
    select uid, access_1d, access_7d, access_30d, title from tabpost order by access_1d DESC limit 10
    '''
    cur.execute(recent_1d)
    recs = cur.fetchall()
    for rec in recs:
        print(rec)

    print('近7日：')
    recent_7d = '''
    select uid, access_1d, access_7d, access_30d, title from tabpost order by access_7d DESC limit 10
    '''
    cur.execute(recent_7d)
    recs = cur.fetchall()
    for rec in recs:
        print(rec)

    print('近30日：')
    recent_30d = '''
    select uid, access_1d, access_7d, access_30d, title from tabpost order by access_7d DESC limit 10
    '''
    cur.execute(recent_30d)
    recs = cur.fetchall()
    for rec in recs:
        print(rec)


def update_view_count():
    cur = DB_CON.cursor()
    ts1d, ts7d, ts30d = ts_helper()

    cur.execute('select uid from tabpost')
    post_ids = []
    for rec in cur.fetchall():
        post_ids.append(rec[0])

    print('更新近24小时')
    for uid in post_ids:
        CUR.execute(
            "select count(*) from tabaccess where post_id = '{}' and uid >= {}".format(
                uid, ts1d
            )
        )
        the_count = CUR.fetchone()[0]

        cur.execute(
            "update tabpost set access_1d = {} where uid = '{}'".format(
                the_count, uid
            )
        )
        # 每次提交。不然似乎导致数据库锁住，长时间无响应。
        DB_CON.commit()

    print('更新近7日')
    for uid in post_ids:
        CUR.execute(
            "select count(*) from tabaccess where post_id = '{}' and uid >= {}".format(
                uid, ts7d
            )
        )
        the_count = CUR.fetchone()[0]

        cur.execute(
            "update tabpost set access_7d = {} where uid = '{}'".format(
                the_count, uid
            )
        )
        # 每次提交。不然似乎导致数据库锁住，长时间无响应。
        DB_CON.commit()

    print('更新近30日')
    for uid in post_ids:
        CUR.execute(
            "select count(*) from tabaccess where post_id = '{}' and uid >= {}".format(
                uid, ts30d
            )
        )
        the_count = CUR.fetchone()[0]

        cur.execute(
            "update tabpost set access_30d = {} where uid = '{}'".format(
                the_count, uid
            )
        )
        # 每次提交。不然似乎导致数据库锁住，长时间无响应。
        DB_CON.commit()


def run_update(_):
    run_sitemap()
    run_editmap()
    update_view_count()
    echo_info()
