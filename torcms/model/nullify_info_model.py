# -*- coding:utf-8 -*-

'''
Model for Posts.
'''

from torcms.model.core_tab import TabPost
from torcms.model.abc_model import Mabc
from config import CMS_CFG


class MNullifyInfo(Mabc):
    '''
    Model for Posts.
    '''

    def __init__(self):
        super(MNullifyInfo, self).__init__()


    @staticmethod
    def query_pager_by_valid(current_page_num=1):

        recs = TabPost.select().where(TabPost.valid == 0).order_by(
            TabPost.time_update.desc()
        ).paginate(current_page_num, CMS_CFG['list_num'])

        return recs

    @staticmethod
    def count_of_certain():

        recs = TabPost.select().where(TabPost.valid == 0)

        return recs.count()