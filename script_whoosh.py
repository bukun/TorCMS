# -*- coding:utf-8 -*-
from torcms.core.tool import run_whoosh
from config import kind_arr, post_type
if __name__ == '__main__':
    run_whoosh.gen_whoosh_database(kind_arr=kind_arr, post_type=post_type)