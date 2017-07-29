# -*- coding: utf-8 -*-

'''
Script for Command.
'''

import sys
import getopt
from .script_migrate import run_migrate
from .script_init import run_init
from .script_sendemail_all import run_send_all, run_send_nologin
from .script_review import run_review
# from .script_create_admin import run_create_admin
from .script_sitemap import run_sitemap
from .script_check_kind import run_check_kind
from .script_fetch_fe2lib import run_f2elib
from .script_init_tabels import run_init_tables
from .script_drop_tabels import run_drop_tables
from .script_gen_category import run_gen_category

from .autocrud.gen_html_file import generate_html_files as run_auto

from .script_whoosh import run_whoosh
from .tmplchecker import run_checkit
from .script_sitemap import run_editmap


def entry(argv):
    '''
    Command entry
    :param argv:
    :return:
    '''
    command_dic = {
        'migrate': run_migrate,
        'init': run_init,
        'send_nologin': run_send_nologin,
        'send_all': run_send_all,
        'edit_diff': run_review,  # Deprecated
        'review': run_review,
        # 'create_admin': run_create_admin,
        'sitemap': run_sitemap,
        'editmap': run_editmap,
        'check_kind': run_check_kind,
        'f2elib': run_f2elib,
        'init_tables': run_init_tables,
        'drop_tables': run_drop_tables,
        'gen_category': run_gen_category,
        'auto': run_auto,
        'whoosh': run_whoosh,
        'check': run_checkit,
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
            print('cmd list ----------------------')
            print('          init: ')
            print('       migrate: ')
            print('        review: ')
            print('         -------------')
            print('      send_all: ')
            print('  send_nologin: ')
            # print('  create_admin: ')
            print('       sitemap: ')
            print('       editmap: ')
            print('    check_kind: ')
            print('         check: ')

            sys.exit()
        elif opt == "-i":

            if arg in command_dic:
                command_dic[arg](args)
                print('QED!')
            else:
                print('Wrong Command.')
