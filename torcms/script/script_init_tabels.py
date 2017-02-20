# -*- coding: utf-8 -*-

'''
initialize table.s
'''

from torcms.model.core_tab import g_Post, g_Tag, g_Member, g_Wiki, g_Link, g_Entity, \
    g_PostHist, g_WikiHist, g_Collect, g_Post2Tag, g_Rel, g_Evaluation, g_Usage, g_Reply, \
    g_User2Reply, g_Rating
from torcms.model.map_tab import e_Layout, e_Json, e_Post2Json


def create_table(Tab):
    try:
        Tab.create_table()
    except:
        pass


def run_init_tables(*args):
    print('--')

    create_table(g_Post)
    create_table(g_Tag)
    create_table(g_Member)
    create_table(g_Wiki)
    create_table(g_Link)
    create_table(g_Entity)
    create_table(g_PostHist)
    create_table(g_WikiHist)
    create_table(g_Collect)
    create_table(g_Post2Tag)
    create_table(g_Rel)
    create_table(g_Evaluation)
    create_table(g_Usage)
    create_table(g_Reply)
    create_table(g_User2Reply)
    create_table(g_Rating)
    create_table(e_Layout)
    create_table(e_Json)
    create_table(e_Post2Json)
