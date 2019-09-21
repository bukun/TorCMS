# -*- coding:utf-8 -*-

'''
Model for referrer.
'''
import peewee
from torcms.core import tools

from torcms.model.abc_model import Mabc, MHelper

from torcms.core.base_model import BaseModel


class Tabreferrer(BaseModel):
    uid = peewee.CharField(null=False, index=False, unique=True, primary_key=True, default='00000',
                           max_length=5, help_text='', )
    media = peewee.CharField(null=False, help_text='来源', )
    terminal = peewee.CharField(null=False, help_text='终端', )
    userip = peewee.CharField(null=False, unique=True, help_text='用户端ip', )
    usercity = peewee.CharField(null=False, help_text='用户端城市', )
    kind = peewee.CharField(null=False, max_length=1,
                            default='1', help_text='', )
    time_create = peewee.IntegerField()


class MReferrer(Mabc):
    @staticmethod
    def get_by_uid(uid):
        '''
        return the record by uid
        '''
        return MHelper.get_by_uid(Tabreferrer, uid)

    @staticmethod
    def modify_meta(uid, data_dic):
        userip = data_dic['userip'].strip()
        if len(userip) < 2:
            return False

        cur_info = MReferrer.get_by_uid(userip)
        if cur_info:
            entry = Tabreferrer.update(
                uid=uid,
                media=data_dic['media'],
                terminal=data_dic['terminal'],
                userip=userip,
                usercity=data_dic['usercity'],
            ).where(Tabreferrer.uid == uid)
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
        Tabreferrer.create(
            uid=uid,
            media=data_dic['media'],
            terminal=data_dic['terminal'],
            userip=userip,
            usercity=data_dic['usercity'],
            kind=data_dic['kind'],
            time_create=tools.timestamp(),
        )
        return uid

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''

        return MHelper.delete(Tabreferrer, uid)

    @staticmethod
    def query_all():
        '''
        query all the posts.
        '''
        return Tabreferrer.select()

    @staticmethod
    def get_by_userip(userip):
        recs = Tabreferrer.select().where(Tabreferrer.userip == userip)
        return recs
