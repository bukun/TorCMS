# -*- coding: utf-8

'''
script for initialization.
'''

from .autocrud.base_crud import build_dir
build_dir()
from torcms.model.core_tab import *
from torcms.model.map_tab import e_Json, e_Layout, e_Post2Json

from .script_gen_category import run_gen_category
from .script_crud import run_auto
from .script_fetch_fe2lib import run_fetch_f2elib

from torcms.core.tool import run_whoosh
from config import kind_arr, post_type

def create_table(Tab):
    try:
        Tab.create_table()
    except:
        pass

def init_tables():
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

def run_init():
    '''
    running init.
    :return:
    '''
    run_fetch_f2elib()
    init_tables()
    run_gen_category()
    run_auto()
    run_whoosh.gen_whoosh_database(kind_arr=kind_arr, post_type=post_type)