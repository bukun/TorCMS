# -*- coding: utf-8 -*-

'''
script for initialization.
'''
from .script_init_tabels import run_init_tables
from .autocrud.base_crud import build_dir
from .script_gen_category import run_gen_category
from .autocrud.gen_html_file import generate_html_files as run_auto
from .script_fetch_fe2lib import run_f2elib
from .script_funcs import run_create_admin, run_whoosh
from .script_migrate import run_migrate

build_dir()


def run_init(*args):
    '''
    running init.
    :return:
    '''
    # run_f2elib()
    run_init_tables()
    run_migrate()
    run_gen_category()
    run_create_admin()
    run_auto()
    run_whoosh()
