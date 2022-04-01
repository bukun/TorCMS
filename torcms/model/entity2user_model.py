# -*- coding:utf-8 -*-
'''
For file entities. Just like pdf, zipfile, docx, etc.
'''

import time
import datetime
from config import CMS_CFG
from torcms.core import tools
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabEntity, TabEntity2User, TabMember


class MEntity2User():
    '''
    For file entities. Just like pdf, zipfile, docx, etc.
    '''

    @staticmethod
    def get_by_uid(uid):
        return MHelper.get_by_uid(TabEntity2User, uid)

    @staticmethod
    def get_by_path(path):
        recs = TabEntity2User.select(
            TabEntity2User,
            TabEntity.path.alias('entity_path'),
            TabEntity.kind.alias('entity_kind'),
        ).join(TabEntity,
               on=(TabEntity2User.entity_id == TabEntity.uid)).where(
            TabEntity.path == path)
        return recs

    @staticmethod
    def query_all(limit=20):
        return TabEntity2User.select().limit(limit)

    @staticmethod
    def get_all_pager(current_page_num=1):
        recs = TabEntity2User.select(
            TabEntity2User, TabEntity.path.alias('entity_path'),
            TabEntity.kind.alias('entity_kind')).join(
            TabEntity,
            on=(TabEntity2User.entity_id == TabEntity.uid)).join(
            TabMember,
            on=(TabEntity2User.user_id == TabMember.uid)).order_by(
            TabEntity2User.timestamp.desc()).paginate(
            current_page_num, CMS_CFG['list_num'])
        return recs

    @staticmethod
    def get_all_pager_by_username(userid, current_page_num=1):
        recs = TabEntity2User.select(
            TabEntity2User,
            TabEntity.path.alias('entity_path'),
            TabEntity.kind.alias('entity_kind'),
        ).join(TabEntity, on=(TabEntity2User.entity_id == TabEntity.uid)).join(
            TabMember, on=(TabEntity2User.user_id == TabMember.uid)).where(
            TabEntity2User.user_id == userid).order_by(
            TabEntity2User.timestamp.desc(),
            TabEntity2User.entity_id).paginate(current_page_num,
                                               CMS_CFG['list_num'])
        return recs

    @staticmethod
    def create_entity2user(enti_uid, user_id, user_ip):
        '''
        create entity2user record in the database.
        '''

        TabEntity2User.create(uid=tools.get_uuid(),
                              entity_id=enti_uid,
                              user_id=user_id,
                              user_ip=user_ip,
                              timestamp=time.time())

    @staticmethod
    def total_number():
        '''
        用户相关的实体总数目
        '''
        return TabEntity2User.select().count()

    @staticmethod
    def total_number_by_user(userid):
        return TabEntity2User.select().where(
            TabEntity2User.user_id == userid).count()

    @staticmethod
    def total_number_by_year(year):
        down_year = int(time.mktime(time.strptime(year, "%Y")))
        next_year = str(int(year) + 1)
        return TabEntity2User.select().where(
            (TabEntity2User.timestamp >= down_year) & (
                    TabEntity2User.timestamp < int(time.mktime(time.strptime(next_year, "%Y")))
            )
        ).count()

    @staticmethod
    def delete_by_uid(entity_uid):
        delete = TabEntity2User.delete().where(
            TabEntity2User.entity_id == entity_uid)
        delete.execute()
