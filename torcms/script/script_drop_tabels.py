# -*- coding: utf-8 -*-
'''
删除所有的表。
'''

from torcms.model.core_tab import (TabCollect, TabEntity, TabEntity2User,
                                   TabEvaluation, TabLink, TabLog, TabMember,
                                   TabPost, TabPost2Tag, TabPostHist,
                                   TabRating, TabReferrer, TabRel, TabReply,
                                   TabReplyid, TabTag, TabUsage, TabUser2Reply,
                                   TabWiki, TabWikiHist, TabCorrelation)


def drop_the_table(table_name):
    '''
    Drop a table.
    '''
    try:
        table_name.drop_table()
    except Exception as err:
        print(repr(err))


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
    drop_the_table(TabLog)
    drop_the_table(TabReferrer)
    drop_the_table(TabEntity2User)
    drop_the_table(TabReplyid)
    drop_the_table(TabCorrelation)
