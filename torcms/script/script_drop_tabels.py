# -*- coding: utf-8 -*-

'''
initialize table.s
'''

from torcms.model.core_tab import TabPost, TabTag, TabMember, TabWiki, TabLink, TabEntity, \
    TabPostHist, TabWikiHist, TabCollect, TabPost2Tag, TabRel, TabEvaluation, TabUsage, TabReply, \
    TabUser2Reply, TabRating


def drop_the_table(table_name):
    '''
    Drop a table.
    '''
    try:
        table_name.drop_table()
    except:
        pass


def run_drop_tables(_):
    '''
    Running the script.
    '''
    print('--')

    drop_the_table(TabPost)
    drop_the_table(TabTag)
    drop_the_table(TabMember)
    drop_the_table(TabWiki)
    drop_the_table(TabLink)
    drop_the_table(TabEntity)
    drop_the_table(TabPostHist)
    drop_the_table(TabWikiHist)
    drop_the_table(TabCollect)
    drop_the_table(TabPost2Tag)
    drop_the_table(TabRel)
    drop_the_table(TabEvaluation)
    drop_the_table(TabUsage)
    drop_the_table(TabReply)
    drop_the_table(TabUser2Reply)
    drop_the_table(TabRating)
