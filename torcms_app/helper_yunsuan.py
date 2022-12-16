# -*- coding: utf-8 -*-

'''
针对本项目的Helper.
'''

import sys

from torcms_app.script.command import entry, run_check_jshtml

kind = 's'
if __name__ == '__main__':
    if len(sys.argv) == 1:
        '''
        缺省情况下，自动运行
        '''
        run_check_jshtml(kind='s')
        # print('run:')
        # print('    python helper.py -h ')
        # print('for help')
    else:
        entry(sys.argv[1:], kind=kind)
