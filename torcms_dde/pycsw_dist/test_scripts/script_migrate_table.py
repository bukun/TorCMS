# -*- coding: utf-8 -*-

from torcms.script.script_init_tabels import create_table
from torcms_dde.model.ext import Records


def run_init_tables(*args):
    '''
    Run to init tables.
    '''

    try:
        create_table(Records)
    except Exception as err:
        print('--------')
        print(repr(err))

    print('Migration finished.')


if __name__ == '__main__':
    run_init_tables()
