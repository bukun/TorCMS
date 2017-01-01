# -*- coding: utf-8

__author__ = 'bukun'

from torcms.model.core_tab import *


def run_init_tables():

    try:
        g_Tag.create_table()
    except:
        pass

    try:
        g_Member.create_table()
    except:
        pass

    try:
        g_Wiki.create_table()
    except:
        pass

    try:
        g_Entity.create_table()
    except:
        pass

    try:
        g_Post.create_table()
    except:
        pass


    try:
        g_PostHist.create_table()
    except:
        pass
    try:
        g_WikiHist.create_table()
    except:
        pass


    try:
        g_Collect.create_table()
    except:
        pass

    try:
        g_Post2Tag.create_table()
    except:
        pass

    try:
        g_Rel.create_table()
    except:
        pass

    try:
        g_Evaluation.create_table()
    except:
        pass

    try:
        g_Usage.create_table()
    except:
        pass

    try:
        g_Reply.create_table()
    except:
        pass

    try:
        g_Wiki.create_table()
    except:
        pass

    try:
        g_Link.create_table()
    except:
        pass

