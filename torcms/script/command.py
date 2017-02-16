# -*- coding: utf-8 -*-

'''
Script for Command.
'''

import sys
import getopt
from .script_migrate import run_migrate
from .script_init import run_init
from .script_sendemail_all import run_send_all, run_send_nologin
from .script_edit_diff import run_edit_diff
from .script_create_admin import run_create_admin
from .script_sitemap import run_sitemap
from .script_check_kind import run_check_kind


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
        'edit_diff': run_edit_diff,
        'create_admin': run_create_admin,
        'sitemap': run_sitemap,
        'check_kind': run_check_kind,
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
            print('          init: ')

            print('       migrate: ')
            print('     edit_diff: ')
            print('      send_all: ')
            print('  send_nologin: ')
            print('  create_admin: ')
            print('       sitemap: ')
            print('    check_kind: ')

            sys.exit()
        elif opt == "-i":

            if arg in command_dic:
                command_dic[arg]()
                print('QED!')
            else:
                print('Wrong Command.')
