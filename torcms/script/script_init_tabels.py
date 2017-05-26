# -*- coding: utf-8 -*-

'''
initialize table.s
'''

from torcms.model.core_tab import TabPost, TabTag, TabMember, TabWiki, TabLink, TabEntity, \
    TabPostHist, TabWikiHist, TabCollect, TabPost2Tag, TabRel, TabEvaluation, TabUsage, TabReply, \
    TabUser2Reply, TabRating


def create_table(Tab):
    try:
        Tab.create_table()
    except:
        pass


def run_init_tables(*args):
    print('--')

    create_table(TabPost)
    create_table(TabTag)
    create_table(TabMember)
    create_table(TabWiki)
    create_table(TabLink)
    create_table(TabEntity)
    create_table(TabPostHist)
    create_table(TabWikiHist)
    create_table(TabCollect)
    create_table(TabPost2Tag)
    create_table(TabRel)
    create_table(TabEvaluation)
    create_table(TabUsage)
    create_table(TabReply)
    create_table(TabUser2Reply)
    create_table(TabRating)

