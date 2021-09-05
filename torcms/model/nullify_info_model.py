# -*- coding:utf-8 -*-
'''
Model for Posts.
'''

from config import CMS_CFG
from torcms.model.core_tab import TabPost


class MNullifyInfo():
    '''
    Model for Posts.
    '''
    def __init__(self):
        super().__init__()

    @staticmethod
    def query_pager_by_valid(current_page_num=1):

        recs = TabPost.select().where(TabPost.valid == 0).order_by(
            TabPost.time_update.desc()).paginate(current_page_num,
                                                 CMS_CFG['list_num'])

        return recs

    @staticmethod
    def count_of_certain():

        recs = TabPost.select().where(TabPost.valid == 0)

        return recs.count()
