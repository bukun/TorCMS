# -*- coding: utf-8 -*-

'''
Script for Command.
'''

import sys
import getopt
from .script_migrate import run_migrate
from .script_gen_category import run_gen_category
from .script_init_database_shema import run_init_tables
from .script_sendemail_all import run_send_all, run_send_nologin
from .script_edit_diff import run_edit_diff
from .script_create_admin import run_create_admin
from .script_fetch_fe2lib import run_fetch_f2elib
from .script_sitemap import run_sitemap
from .script_check_kind import run_check_kind
from .script_crud import run_crud1, run_crud0
from .script_nocat import run_nocat
from .script_code_line import run_lines


def entry(argv):
    '''
    Command entry
    :param argv:
    :return:
    '''
    command_dic = {
        'migrate': run_migrate,
        'gen_category': run_gen_category,
        'init_tables': run_init_tables,
        'send_nologin': run_send_nologin,
        'send_all': run_send_all,
        'edit_diff': run_edit_diff,
        'create_admin': run_create_admin,
        'fetch_f2elib': run_fetch_f2elib,
        'sitemap': run_sitemap,
        'check_kind': run_check_kind,
        'crud0': run_crud0,
        'crud1': run_crud1,
        'nocat': run_nocat,
        'lines': run_lines
    }
    try:
        # 这里的 h 就表示该选项无参数，i:表示 i 选项后需要有参数
        opts, args = getopt.getopt(argv, "hi:")
    except getopt.GetoptError:
        print('Error: helper.py -i cmd')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print('helper.py -i cmd')
            print('cmd list----------------------')
            print('  fetch_f2elib: ')
            print('       migrate: ')
            print('     edit_diff: ')
            print('  gen_category: ')
            print('   init_tables: ')
            print('      send_all: ')
            print('  send_nologin: ')
            print('  create_admin: ')
            print('       sitemap: ')
            print('    check_kind: ')
            print('         crud0: ')
            print('         crud1: ')
            print('         nocat: ')
            print('         lines: ')

            sys.exit()
        elif opt == "-i":

            if arg in command_dic:
                command_dic[arg]()
                print('QED!')
            else:
                print('Wrong Command.')
