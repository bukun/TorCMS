# -*- coding: utf-8 -*-

'''
running whoosh
'''
from config import kind_arr, post_type
from torcms.core.tool import run_whoosh as running_whoosh


def run_whoosh(*args):
    '''
    running whoosh
    '''
    running_whoosh.gen_whoosh_database(kind_arr=kind_arr, post_type=post_type)
