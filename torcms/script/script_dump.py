# -*- coding: utf-8 -*-
'''
Dump database of PostgreSQL, with date stamp.
'''
import datetime
import os
import subprocess

try:
    from cfg import DB_CFG
except Exception as err:
    print(repr(err))
    DB_CFG = {
        'db': '',
        'pass': '',
    }

if os.path.exists('tmp'):
    pass
else:
    os.mkdir('tmp')


def run_dump(_):
    '''
    Dump database of PostgreSQL
    '''
    print('Dumping ... ')

    current = datetime.datetime.now()
    dstr = '{}{}{}-{}{}'.format(current.year, current.month, current.day,
                                current.hour, current.minute)
    cmd = 'export PGPASSWORD={p} && pg_dump -h localhost -F c -U {n} {n} > ./tmp/xx_pg_{n}_{d}.bak'.format(
        n=DB_CFG['db'], p=DB_CFG['pass'], d=dstr)
    subprocess.run(cmd, shell=True)
