# -*- coding:utf-8 -*-

'''
For file entities. Just like pdf, zipfile, docx, etc.
'''

import time
from torcms.model.core_tab import TabEntity
from torcms.model.abc_model import Mabc, MHelper
from torcms.core.tools import logger


class MEntity(Mabc):
    '''
    For file entities. Just like pdf, zipfile, docx, etc.
    '''

    @staticmethod
    def query_all(limit=20):
        return TabEntity.select().limit(limit)

    @staticmethod
    def get_id_by_impath(path):
        logger.info('Get Entiry, Path: {0}'.format(path))

        uu = TabEntity.select().where(TabEntity.path == path)
        if uu.count() == 1:
            return uu.get().uid
        elif uu.count() > 1:
            for rec in uu:
                MEntity.delete(rec.uid)
            return False
        else:
            return False

    @staticmethod
    def create_entity(signature, impath, kind='1'):
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
                time_create=time.time(),
                kind=kind
            )
            return True
        except:
            return False

    @staticmethod
    def delete(uid):
        return MHelper.delete(TabEntity, uid)
