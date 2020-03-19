# -*- coding:utf-8 -*-

'''
For file entities. Just like pdf, zipfile, docx, etc.
'''

import time
from torcms.model.core_tab import TabEntity2User
from torcms.model.core_tab import TabEntity
from torcms.model.core_tab import TabMember
from torcms.model.abc_model import Mabc, MHelper
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
    def get_all_pager(current_page_num=1):

        recs = TabEntity2User.select(
            TabEntity2User,
            TabEntity.path.alias('entity_path'),
            TabEntity.kind.alias('entity_kind')
        ).join(TabEntity, on=(TabEntity2User.entity_id == TabEntity.uid)).join(
            TabMember, on=(TabEntity2User.user_id == TabMember.uid)
        ).order_by(
            TabEntity2User.timestamp.desc()
        ).paginate(current_page_num, CMS_CFG['list_num'])
        return recs

    @staticmethod
    def get_all_pager_by_username(userid, current_page_num=1):

        recs = TabEntity2User.select(
            TabEntity2User,
            TabEntity.path.alias('entity_path'),
            TabEntity.kind.alias('entity_kind'),
        ).join(TabEntity, on=(TabEntity2User.entity_id == TabEntity.uid)).join(
            TabMember, on=(TabEntity2User.user_id == TabMember.uid)
        ).where(TabEntity2User.user_id == userid).order_by(
            TabEntity2User.entity_id
        ).paginate(current_page_num, CMS_CFG['list_num'])
        return recs


    @staticmethod
    def create_entity2user(enti_uid, user_id, user_ip):
        '''
        create entity2user record in the database.
        '''

        TabEntity2User.create(
            uid=tools.get_uuid(),
            entity_id=enti_uid,
            user_id=user_id,
            user_ip=user_ip,
            timestamp=time.time()
        )

    @staticmethod
    def total_number():
        return TabEntity2User.select().count()

    @staticmethod
    def total_number_by_user(userid):
        return TabEntity2User.select().where(TabEntity2User.user_id == userid).count()

    @staticmethod
    def delete_by_uid(entity_uid):
        delete = TabEntity2User.delete().where(TabEntity2User.entity_id == entity_uid)
        delete.execute()
