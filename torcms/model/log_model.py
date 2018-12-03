# -*- coding:utf-8 -*-

'''
Rating for post.
'''

import peewee
from torcms.core import tools
from torcms.model.core_tab import TabLog
from torcms.model.abc_model import Mabc


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
