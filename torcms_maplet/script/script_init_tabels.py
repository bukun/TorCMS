# -*- coding: utf-8 -*-

'''
initialize table.s
'''

from torcms_maplet.model.map_tab import MabGson, MabLayout, MabPost2Gson


def create_table(Tab):
    try:
        Tab.create_table()
    except Exception:
        pass


def run_init_tables(*args):
    print('--')

    create_table(MabLayout)
    create_table(MabGson)
    create_table(MabPost2Gson)
