# -*- coding:utf-8 -*-

'''
Rating for post.
'''

import peewee
from torcms.core import tools
from torcms.model.core_tab import TabLog
from config import CMS_CFG, DB_CFG
from torcms.model.abc_model import Mabc, MHelper


class MLog(Mabc):
    '''
    用户日志
    '''

    @staticmethod
    def insert_data(userid, postid, kind):
        '''
        Insert new record.
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
    def add(data_dic):
        '''
        Insert new record.
        '''

        uid = data_dic['uid']
        TabLog.create(
            uid=uid,
            current_url=data_dic['url'],
            refer_url=data_dic['refer'],
            user_id=data_dic['user_id'],
            time_create=data_dic['timein'],
            time_out=data_dic['timeOut'],
            time=data_dic['timeon']
        )

        return uid

    @staticmethod
    def query_pager_by_user(userid, current_page_num=1):
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

    @staticmethod
    def get_by_uid(uid):
        '''
        return the record by uid
        '''
        return MHelper.get_by_uid(TabLog, uid)

    @staticmethod
    def get_retention_time_by_id(uid, user_id):
        current_rec = MLog.get_by_uid(uid)
        recs = TabLog.select().where(
            (TabLog.user_id == user_id) &
            (TabLog.time_create > current_rec.time_create)
        ).order_by(TabLog.time_create)
        if recs.count():
            return recs.get()
        return None
