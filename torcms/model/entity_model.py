# -*- coding:utf-8 -*-

'''
For file entities. Just like pdf, zipfile, docx, etc.
'''

import time
from torcms.model.core_tab import g_Entity
from torcms.model.abc_model import Mabc, MHelper
from torcms.core.tools import logger


class MEntity(Mabc):
    '''
    For file entities. Just like pdf, zipfile, docx, etc.
    '''

    def __init__(self):
        try:
            g_Entity.create_table()
        except:
            pass

    @staticmethod
    def query_all(limit=20):
        return g_Entity.select().limit(limit)

    @staticmethod
    def get_id_by_impath(path):
        logger.info('Get Entiry, Path: {0}'.format(path))

        uu = g_Entity.select().where(g_Entity.path == path)
        if uu.count() == 1:
            return uu.get().uid
        elif uu.count() > 1:
            for rec in uu:
                MEntity.delete(rec.uid)
            return False
        else:
            return False

    @staticmethod
    def create_wiki_history(signature, impath, kind='1'):
        if len(impath) == 0:
            return False

        try:
            g_Entity.create(
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
        return MHelper.delete(g_Entity, uid)
