# -*- coding: utf-8
import sys
from torcms.script.command import entry

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('run:')
        print('    python helper.py -h ')
        print('for help')
        print('=' * 79)
        entry(['-i', 'init'])
    else:
        entry(sys.argv[1:])
