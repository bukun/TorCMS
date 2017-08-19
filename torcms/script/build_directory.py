# -*- coding: utf-8 -*-
'''
Build the directory for Whoosh database.
and locale.
'''
import os

WHOOSH_DB_DIR = 'database/whoosh'


def build_directory():
    if os.path.exists('locale'):
        pass
    else:
        os.mkdir('locale')
    if os.path.exists(WHOOSH_DB_DIR):
        pass
    else:
        os.makedirs(WHOOSH_DB_DIR)
