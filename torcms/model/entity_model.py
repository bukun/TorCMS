# -*- coding:utf-8 -*-
'''
For file entities. Just like pdf, zipfile, docx, etc.
'''

import time

from config import CMS_CFG
from torcms.core.tools import get_uuid, logger
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabEntity


class MEntity():
    '''
    For file entities. Just like pdf, zipfile, docx, etc.
    '''
    @staticmethod
    def get_by_uid(uid):
        return MHelper.get_by_uid(TabEntity, uid)

    @staticmethod
    def query_all(limit=20):
        '''
        Return the entities list.
        '''
        return TabEntity.select().limit(limit)

    @staticmethod
    def get_by_kind(kind=1, current_page_num=1):
        return TabEntity.select().where(TabEntity.kind == kind).paginate(
            current_page_num, CMS_CFG['list_num'])

    @staticmethod
    def get_all_pager(current_page_num=1):
        return TabEntity.select().paginate(current_page_num,
                                           CMS_CFG['list_num'])

    @staticmethod
    def get_id_by_impath(path):
        '''
        The the entity id by the path.
        '''
        logger.info('Get Entiry, Path: {0}'.format(path))

        entity_list = TabEntity.select().where(TabEntity.path == path)
        out_val = None
        if entity_list.count() == 1:
            out_val = entity_list.get()
        elif entity_list.count() > 1:
            for rec in entity_list:
                MEntity.delete(rec.uid)
            out_val = None
        else:
            pass
        return out_val

    @staticmethod
    def create_entity(uid='', path='', desc='', kind='1'):
        '''
        create entity record in the database.
        '''

        if path:
            pass
        else:
            return False

        if uid:
            pass
        else:
            uid = get_uuid()
        try:
            TabEntity.create(uid=uid,
                             path=path,
                             desc=desc,
                             time_create=time.time(),
                             kind=kind)
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def delete(uid):
        return MHelper.delete(TabEntity, uid)

    @staticmethod
    def total_number():
        '''
        Total number.
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        return TabEntity.select().count(None)

    @staticmethod
    def delete_by_path(path, kind='f'):
        '''
        '''
        delete = TabEntity.delete().where((TabEntity.path == path)
                                          & (TabEntity.kind == kind))

        delete.execute()
