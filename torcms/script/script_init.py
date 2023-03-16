'''
script for initialization.
'''

import sys

from config import DB_CON

from .autocrud.base_crud import build_dir
from .autocrud.gen_html_file import generate_html_files as run_auto
from .script_funcs import run_create_admin, run_whoosh
from .script_gen_category import run_gen_category
from .script_init_tabels import run_init_tables
from .script_zero import run_zero


def run_init(*args):
    '''
    running init.
    '''
    build_dir()
    run_auto()

    try:
        DB_CON.cursor()
    except Exception as err:
        print(repr(err))
        print('Could not connect to database ...')
        run_zero()
        sys.exit()

    run_init_tables()
    run_gen_category()
    run_create_admin()
    run_whoosh()
