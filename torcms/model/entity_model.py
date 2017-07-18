# -*- coding:utf-8 -*-

'''
For file entities. Just like pdf, zipfile, docx, etc.
'''

import time
from torcms.model.core_tab import TabEntity
from torcms.model.abc_model import Mabc, MHelper
from torcms.core.tools import logger
from config import CMS_CFG

class MEntity(Mabc):
    '''
    For file entities. Just like pdf, zipfile, docx, etc.
    '''
    @staticmethod
    def get_by_uid(uid):
        return MHelper.get_by_uid(TabEntity, uid)
    @staticmethod
    def query_all(limit=20):
        return TabEntity.select().limit(limit)

    @staticmethod
    def get_by_kind(current_page_num=1):
        return TabEntity.select().paginate(current_page_num, CMS_CFG['list_num'])

    @staticmethod
    def get_id_by_impath(path):
        logger.info('Get Entiry, Path: {0}'.format(path))

        entity_list = TabEntity.select().where(TabEntity.path == path)
        if entity_list.count() == 1:
            return entity_list.get().uid
        elif entity_list.count() > 1:
            for rec in entity_list:
                MEntity.delete(rec.uid)
            return False
        else:
            return False

    @staticmethod
    def create_entity(signature, impath, img_desc, kind='1'):
        '''
        create entity record in the database.
        :param signature:
        :param impath:
        :param kind:
        :return:
        '''
        if len(impath) == 0:
            return False

        try:
            TabEntity.create(
                uid=signature,
                path=impath,
                desc=img_desc,
                time_create=time.time(),
                kind=kind
            )
            return True
        except:
            return False

    @staticmethod
    def delete(uid):
        return MHelper.delete(TabEntity, uid)

    @staticmethod
    def total_number():
        return TabEntity.select().count()
