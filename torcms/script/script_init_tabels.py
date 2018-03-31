# -*- coding: utf-8 -*-

'''
initialize table.s
'''

from torcms.model.core_tab import TabPost, TabTag, TabMember, TabWiki, TabLink, TabEntity, \
    TabPostHist, TabWikiHist, TabCollect, TabPost2Tag, TabRel, TabEvaluation, TabUsage, TabReply, \
    TabUser2Reply, TabRating, TabEntity2User


def create_table(the_table):
    '''
    Create a certain table.
    '''
    try:
        the_table.create_table()
    except:
        pass


def run_init_tables(*args):
    '''
    Run to init tables.
    '''
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
    create_table(TabEntity2User)
