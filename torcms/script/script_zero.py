# -*- coding: utf-8 -*-

'''
Generate some helper files.
'''

from cfg import DB_CFG


def run_zero(_):
    '''
    Generate some helper files.
    '''
    if "'" in DB_CFG['pass']:
        print("There should be no ``'`` in password. Be careful.")

    the_str = '''CREATE USER {db} WITH PASSWORD '{passwd}' ;
CREATE DATABASE {db} OWNER {db} ;
GRANT ALL PRIVILEGES ON DATABASE {db} to {db} ;
\c {db} ;
create extension hstore;
    '''.format(db=DB_CFG['db'], passwd=DB_CFG['pass'])

    with open('xx_create_db.sql', 'w') as fo:
        fo.write(
            the_str
        )
