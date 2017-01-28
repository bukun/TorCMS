# -*- coding: utf-8

__author__ = 'bukun'

from torcms.model.core_tab import *

def create_table(Tab):
    try:
        print('Try to create table:' )
        print(' ' * 4 + Tab.__name__)
        Tab.create_table()
        print(' ' * 4 + 'Created')
    except:
        pass

def run_init_tables():

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
