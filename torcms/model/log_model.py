# -*- coding:utf-8 -*-

'''
Rating for post.
'''

import peewee
from torcms.core import tools
from torcms.model.core_tab import TabLog
from torcms.model.abc_model import Mabc
from config import CMS_CFG, DB_CFG


class MLog(Mabc):
    '''
    用户日志
    '''

    @staticmethod
    def insert_data(userid, postid, kind):
        '''
        Inert new record.
        '''
        uid = tools.get_uuid()
        TabLog.create(
            uid=uid,
            post_id=postid,
            user_id=userid,
            kind=kind,
            time_create=tools.timestamp()
        )
        return uid

    @staticmethod
    def query_pager_by_user(userid,current_page_num=1):
        '''
        Query pager
        '''
        return TabLog.select().where(TabLog.user_id == userid).order_by(
            TabLog.time_create.desc()
        ).paginate(
            current_page_num, CMS_CFG['list_num']
        )
    @staticmethod
    def query_all_user(current_page_num=1):
        '''
        Query pager
        '''
        return TabLog.select().distinct(TabLog.user_id).order_by(
            TabLog.user_id
        ).paginate(
            current_page_num, CMS_CFG['list_num']
        )
    @staticmethod
    def total_number():
        '''
        Return the number of certian slug.
        '''
        return TabLog.select().count()

    @staticmethod
    def count_of_certain(user_id):
        recs = TabLog.select().where(TabLog.user_id == user_id)

        return recs.count()
