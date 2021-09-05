# -*- coding:utf-8 -*-
'''
Model for referrer.
'''

from torcms.core import tools
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabReferrer


class MReferrer():
    @staticmethod
    def get_by_uid(uid):
        '''
        return the record by uid
        '''
        return MHelper.get_by_uid(TabReferrer, uid)

    @staticmethod
    def modify_meta(uid, data_dic):
        userip = data_dic['userip'].strip()
        if len(userip) < 2:
            return False

        cur_info = MReferrer.get_by_uid(uid)
        if cur_info:
            entry = TabReferrer.update(
                uid=uid,
                media=data_dic['media'],
                terminal=data_dic['terminal'],
                userip=userip,
                # usercity=data_dic['usercity'],
                kind=data_dic['kind'],
                time_update=tools.timestamp(),
            ).where(TabReferrer.uid == uid)
            entry.execute()

        else:
            return MReferrer.add_meta(uid, data_dic)
        return uid

    @staticmethod
    def add_meta(uid, data_dic):
        if len(uid) < 4:
            return False
        userip = data_dic['userip'].strip()
        if len(userip) < 2:
            return False
        TabReferrer.create(
            uid=uid,
            media=data_dic['media'],
            terminal=data_dic['terminal'],
            userip=userip,
            # usercity=data_dic['usercity'],
            kind=data_dic['kind'],
            time_create=tools.timestamp(),
            time_update=tools.timestamp(),
        )
        return uid

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''

        return MHelper.delete(TabReferrer, uid)

    @staticmethod
    def query_all():
        '''
        query all the posts.
        '''
        return TabReferrer.select()

    @staticmethod
    def get_by_userip(userip):
        recs = TabReferrer.select().where(TabReferrer.userip == userip)
        return recs
