# -*- coding: utf-8 -*-

'''
initialize table.s
'''

from torcms_maplet.model.map_tab import MabLayout, MabGson, MabPost2Gson


def drop_the_table(Tab):
    try:
        Tab.drop_table()
    except Exception:
        pass


def run_drop_tables(*args):
    print('--')

    drop_the_table(MabLayout)
    drop_the_table(MabGson)
    drop_the_table(MabPost2Gson)
