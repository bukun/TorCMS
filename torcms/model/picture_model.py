# -*- coding:utf-8 -*-

import time
from torcms.model.core_tab import g_Entity
from torcms.model.supertable_model import MSuperTable

class MEntity(MSuperTable):
    def __init__(self):
        self.tab = g_Entity
        try:
            g_Entity.create_table()
        except:
            pass

    def getall(self):
        return g_Entity.select()

    def get_id_by_impath(self, path):
        uu = g_Entity.select().where(g_Entity.path == path)
        if uu.count() == 1:
            return uu.get().uid
        elif uu.count() > 1:
            return False
        else:
            return False

    def insert_data(self, signature, impath,kind = '1'):
        entry = g_Entity.create(
            uid=signature,
            path=impath,
            time_create=time.time(),
            kind = kind,
        )
        return entry
