# -*- coding:utf-8 -*-

'''
For file entities. Just like pdf, zipfile, docx, etc.
'''

import time
from torcms.model.core_tab import TabEntity2User
from torcms.model.abc_model import Mabc, MHelper
from torcms.core.tools import logger
from torcms.core import tools
from config import CMS_CFG


class MEntity2User(Mabc):
    '''
    For file entities. Just like pdf, zipfile, docx, etc.
    '''

    @staticmethod
    def get_by_uid(uid):
        return MHelper.get_by_uid(TabEntity2User, uid)

    @staticmethod
    def query_all(limit=20):
        return TabEntity2User.select().limit(limit)

    @staticmethod
    def get_by_kind(kind=1, current_page_num=1):
        return TabEntity2User.select().where(TabEntity2User.kind == kind).paginate(current_page_num, CMS_CFG['list_num'])

    @staticmethod
    def get_all_pager(current_page_num=1):
        return TabEntity2User.select().paginate(current_page_num, CMS_CFG['list_num'])

    @staticmethod
    def count_increate(rec, num):
        entry = TabEntity2User.update(
            timestamp=int(time.time()),
            count=num + 1
        ).where(TabEntity2User.uid == rec)
        entry.execute()

    @staticmethod
    def create_entity2user(enti_uid, user_id):
        '''
        create entity record in the database.
        :param signature:
        :param enti_path:
        :param kind:
        :return:
        '''
        record = TabEntity2User.select().where(
            (TabEntity2User.entity_id == enti_uid) & (TabEntity2User.user_id == user_id)
        )


        if record.count() > 0:
            record = record.get()
            print("*" * 50)
            print(record.count)
            print("*" * 50)
            MEntity2User.count_increate(record.uid, record.count)
        else:
            TabEntity2User.create(
                uid=tools.get_uuid(),
                entity_id=enti_uid,
                user_id=user_id,
                count=1,
                timestamp=time.time()
            )


    @staticmethod
    def delete(uid):
        return MHelper.delete(TabEntity2User, uid)

    @staticmethod
    def total_number():
        return TabEntity2User.select().count()
