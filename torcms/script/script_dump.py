# -*- coding: utf-8 -*-

'''
Dump database of PostgreSQL
'''
import os
from cfg import DB_CFG
import subprocess
import datetime 

if os.path.exists('tmp'):
    pass
else:
    os.mkdir('tmp')

def run_dump(_):
    '''
    Dump database of PostgreSQL
    '''
    print('Dumping ... ')

    i = datetime.datetime.now() 
    dstr = '{}{}{}-{}{}'.format(i.year, i.month, i.day, i.hour, i.minute)
    cmd = 'export PGPASSWORD={p} && pg_dump -h localhost -F c -U {n} {n} > ./tmp/xx_pg_{n}_{d}.bak'.format(
            n = DB_CFG['db'], 
            p = DB_CFG['pass'],
            d = dstr
        )
    subprocess.run(cmd,  shell = True)
