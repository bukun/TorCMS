'''
数据量大的时候比较慢，
按脚本运行。
'''

import psycopg2
import time

from cfg import DB_CFG

conn = psycopg2.connect(
    database=DB_CFG['db'],
    user=DB_CFG['user'],
    password=DB_CFG['pass'],
    host="127.0.0.1",
    port="5432"
)

cur = conn.cursor()

timestamp = int(time.time())
ts1d = timestamp - 24 * 60 * 60
ts7d = timestamp - 7 * 24 * 60 * 60
ts30d = timestamp - 30 * 24 * 60 * 60

更新语句 = '''
UPDATE tabpost SET view_count_1d=(SELECT count(*) FROM tabaccess WHERE (tabaccess.post_id = tabpost.uid) and (tabaccess.uid >= {}));
'''.format(ts1d)
cur.execute(更新语句)

更新语句 = '''
UPDATE tabpost SET view_count_7d=(SELECT count(*) FROM tabaccess WHERE (tabaccess.post_id = tabpost.uid) and (tabaccess.uid >= {}));
'''.format(ts7d)
cur.execute(更新语句)

更新语句 = '''
UPDATE tabpost SET view_count_30d=(SELECT count(*) FROM tabaccess WHERE (tabaccess.post_id = tabpost.uid) and (tabaccess.uid >= {}));
'''.format(ts30d)
cur.execute(更新语句)

conn.commit()

print('QED')

print('近24小时：')
近24小时 = '''
select uid, view_count_1d, view_count_7d, view_count_30d, title from tabpost order by view_count_1d DESC limit 10
'''
cur.execute(近24小时)
recs = cur.fetchall()
for rec in recs:
    print(rec)

print('近7日：')
近7日 = '''
select uid, view_count_1d, view_count_7d, view_count_30d, title from tabpost order by view_count_7d DESC limit 10
'''
cur.execute(近7日)
recs = cur.fetchall()
for rec in recs:
    print(rec)

print('近30日：')
近30日 = '''
select uid, view_count_1d, view_count_7d, view_count_30d, title from tabpost order by view_count_7d DESC limit 10
'''
cur.execute(近30日)
recs = cur.fetchall()
for rec in recs:
    print(rec)
