'''
对Django与TorCMS建立的数据库进行比较
'''

import difflib

import psycopg2
from cfg import DB_INFO

# 连接数据库的参数

dbname = DB_INFO['NAME']
user = DB_INFO['USER']
password = DB_INFO['PASSWORD']
host = DB_INFO['HOST']
port = 5432

# 连接字符串
conn_string = f"host={host} port={port} dbname={dbname} user={user} password={password}"
conn_string2 = (
    f"host={host} port={port} dbname='torcms2' user=torcms2 password={password}"
)

# 建立连接
conn1 = psycopg2.connect(conn_string)
conn2 = psycopg2.connect(conn_string2)


def get_table_structure(conn, table):
    cur = conn.cursor()
    # SELECT column_name, data_type, is_nullable, column_default, is_identity
    cur.execute(
        f"""
        SELECT *        
        FROM information_schema.columns
        WHERE table_name = '{table}'
        ORDER BY ordinal_position;
    """
    )
    columns = cur.fetchall()
    # for rec in columns:
    #     print(rec)
    cur.close()
    return columns


def chuli(tab):
    table1 = get_table_structure(conn1, tab)
    table2 = get_table_structure(conn2, tab)

    t1 = list(map(str, table1))
    t2 = list(map(str, table2))
    print('=' * 20)
    print(t1)
    print('-' * 20)
    print(t2)

    return t1, t2


arr1 = list()
arr2 = list()

table_lsit = [
    'tabpost',
    'tabmember',
    'tabreply',
    'tablog',
    'tabtag',
    'tabpost2tag',
    'tabpost2catalog',
    'tabcatalog',
    'tabuser2catalog',
    'tabuser2reply',
    'tabuser2post',
    'tabuser2tag',
    'tabuser2user',
    'tabuser2role',
    'tabrole2permission',
    'tabstaff2role',
    'tabrole',
    'tabpermission',
    'tabuser',
    'tabuser2permission',
    'tabuser2role',
    'tabrole2permission',
    'tabstaff2role',
    'tabrole',
    'tabpermission',
    'tabuser',
    'tabuser2permission',
    'tabuser2role',
    'tabrole2permission',
    'tabstaff2role',
    'tabrole',
    'tabpermission',
    'tabuser',
    'tabuser2permission',
    'tabuser2role',
    'tabrole2permission',
    'tabstaff2role',
    'tabrole',
    'tabpermission',
    'tabuser',
    'tabuser2permission',
    'tabuser2role',
    'tabrole2permission',
    'tabstaff2role',
    'tabrole',
    'tabpermission',
    'tabuser',
    'tabuser2permission',
    'tabuser2role',
    'tabrole2permission',
    'tabstaff2role',
    'tabrole',
    'tabpermission',
]
# table_lsit = ['tabpost']
for tabname in table_lsit:
    t1, t2 = chuli(tabname)
    arr1 += t1
    arr2 += t2


d = difflib.HtmlDiff()

diff = d.make_file(arr1, arr2)

with open('xx_pgdb_diff.html', 'w') as f:
    f.write(diff)


conn1.close()
