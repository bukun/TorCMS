# -*- coding:utf-8 -*-

'''
The celery routines used in TorCMS.
'''

from celery import Celery
from torcms.core.tool import run_whoosh
# app = Celery('tasks', broker='amqp://guest@localhost//')
app = Celery('tasks', broker='redis://localhost:6379/0')

from config import kind_arr, post_type

@app.task
def cele_gen_whoosh():
    print('run_whoosh.')

    run_whoosh.gen_whoosh_database(kind_arr=kind_arr, post_type=post_type)
