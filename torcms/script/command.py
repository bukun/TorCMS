# -*- coding: utf-8 -*-

import sys, getopt

from .script_migrate import run_migrate
from .script_gen_category import run_gen_category
from .script_init_database_shema import run_init_tables
from .script_update_count import run_update_count
from .script_sendemail_all import run_send_all, run_send_nologin
from .script_edit_diff import run_edit_diff
from .script_create_admin import run_create_admin
from .script_fetch_fe2lib import run_fetch_f2elib
from .script_sitemap import run_sitemap
from .script_check_kind import run_check_kind
from .script_crud import run_crud
from .script_nocat import run_nocat


def entry(argv):
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
            print('    migrate_db: ')
            print('     edit_diff: ')
            print('  gen_category: ')
            print('   init_tables: ')
            print('  update_count: ')
            print('      send_all: ')
            print('  send_nologin: ')
            print('  create_admin: ')
            print('       sitemap: ')
            print('    check_kind: ')
            print('          crud: ')
            print('         nocat: ')

            sys.exit()
        elif opt in ("-i"):
            helper_app = arg
            eval('run_' + helper_app + '()')
