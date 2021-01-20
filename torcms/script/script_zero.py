# -*- coding: utf-8 -*-
'''
Generate some helper files.
'''

try:
    from cfg import DB_CFG
except Exception as err:
    print(repr(err))
    DB_CFG = {
        'db': '',
        'pass': '',
    }


def run_zero():
    '''
    Generate some helper files.
    '''
    if "'" in DB_CFG['pass']:
        print("There should be no ``'`` in password. Be careful.")

    the_str = r'''CREATE USER {db} WITH PASSWORD '{passwd}' ;
CREATE DATABASE {db} OWNER {db} ;
GRANT ALL PRIVILEGES ON DATABASE {db} to {db} ;
\c {db} ;
create extension hstore;
    '''.format(db=DB_CFG['db'], passwd=DB_CFG['pass'])

    with open('xx_create_db.sql', 'w') as fo:
        fo.write(the_str)
    print('\033[33m' '打开 xx_create_db.sql 文件，查看创建数据库的命令。' '\033[0m')
