# -*- coding: utf-8 -*-
'''
Entry for command script.
'''

import getopt
import sys

from .script_init import run_init


def entry(argv):
    '''
    Command entry
    '''
    command_dic = {
        'init': run_init,
    }
    try:
        # 这里的 h 就表示该选项无参数，i:表示 i 选项后需要有参数
        opts, args = getopt.getopt(argv, "hi:")
    except getopt.GetoptError:
        print('Error: helper.py -i cmd')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print()
            print('\033[33m', 'python helper.py -i cmd', '\033[0m')
            print()
            print('---- command list --------------')
            print('\033[33m', '         init: (初始化网站)', '\033[0m')
            print('\033[33m', '       review: (检查网站更新的内容)', '\033[0m')
            print('            --:--               ')
            print('         check: (检查网站问题)')
            print('        update: (更新访问次数等)')
            print('          dump: (备份数据库)')
            print('\033[31m', '        reset: (Danger! drop all tables!)', '\033[0m')

            sys.exit()
        elif opt == "-i":
            if arg in command_dic:
                command_dic[arg](args)
                print('QED!')
            else:
                print('Wrong Command.')
