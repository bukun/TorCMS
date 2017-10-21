# coding:utf-8

'''
The UI methods.
'''

import tornado.escape


def unescape(_, the_str):
    '''
    Unescape .
    '''
    return tornado.escape.xhtml_unescape(the_str)
