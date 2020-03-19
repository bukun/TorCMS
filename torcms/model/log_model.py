# -*- coding:utf-8 -*-

'''
Rating for post.
'''

import peewee
from torcms.core import tools
from torcms.model.core_tab import TabLog
from config import CMS_CFG, DB_CFG
from torcms.model.abc_model import Mabc, MHelper


class MLog():
    '''
    Log for user action.
    '''

    @staticmethod
    def add(data_dic):
        '''
        Insert new record.
        '''
        # uid = data_dic['uid']
        uid = uid = tools.get_uuid()
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
    def query_all_user():
        '''
        查询所有登录用户的访问记录
        ToDo:  ``None`` ?
        '''
        return TabLog.select().where(TabLog.user_id != 'None').distinct(TabLog.user_id).order_by(
            TabLog.user_id
        )

    @staticmethod
    def query_all(current_page_num=1):
        '''
        查询所有未登录用户的访问记录
        ToDo:  ``None`` ?
        '''
        return TabLog.select().where(TabLog.user_id == 'None').order_by(TabLog.time_out.desc()).paginate(
            current_page_num, CMS_CFG['list_num']
        )

    @staticmethod
    def query_all_pageview(current_page_num=1):
        '''
        查询所有页面（current_url），分页
        '''
        return TabLog.select().distinct(TabLog.current_url).order_by(TabLog.current_url).paginate(
            current_page_num, CMS_CFG['list_num']
        )

    @staticmethod
    def query_all_current_url():
        '''
        查询所有页面（current_url）
        '''
        return TabLog.select().distinct(TabLog.current_url).order_by(TabLog.current_url)

    @staticmethod
    def count_of_current_url(current_url):
        '''
        长询制订页面（current_url）的访问量
        '''
        res = TabLog.select().where(TabLog.current_url == current_url)
        return res.count()

    @staticmethod
    def total_number():
        '''
        Return the number of Tablog.
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        return TabLog.select().count(None)

    @staticmethod
    def count_of_certain(user_id):
        recs = TabLog.select().where(TabLog.user_id == user_id)

        return recs.count()

    @staticmethod
    def count_of_certain_pageview():
        recs = TabLog.select().distinct(TabLog.current_url).order_by(TabLog.current_url)

        return recs.count()

    @staticmethod
    def get_by_uid(uid):
        '''
        return the record by uid
        '''
        return MHelper.get_by_uid(TabLog, uid)

    @staticmethod
    def get_pageview_count(current_url):
        recs = TabLog.select().where(TabLog.current_url == current_url)

        return recs.count()
