# -*- coding:utf-8 -*-
'''
Model for referrer.
'''
import peewee

from torcms.core import tools
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabReplyid


class MReplyid():
    @staticmethod
    def get_by_uid(uid):
        '''
        return the record by uid
        '''
        return MHelper.get_by_uid(TabReplyid, uid)

    @staticmethod
    def create_replyid(pid, rid):
        uid = tools.get_uuid()
        TabReplyid.create(
            uid=uid,
            reply0=pid,
            reply1=rid,
            time_create=tools.timestamp(),
        )

    @staticmethod
    def get_by_rid(rid):
        return TabReplyid.select().where(TabReplyid.reply0 == rid).order_by(TabReplyid.time_create.desc())
