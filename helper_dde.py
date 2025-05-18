# -*- coding: utf-8
import sys

from torcms_dde.script.command import entry

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('run:')
        print('    python helper.py -h ')
        print('for help')
    else:
        entry(sys.argv[1:])
