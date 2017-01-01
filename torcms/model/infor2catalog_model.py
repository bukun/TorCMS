# -*- coding:utf-8 -*-


from torcms.model.core_tab import g_Post, g_Tag, g_Post2Tag
from torcms.model.post2catalog_model import MPost2Catalog


class MInfor2Catalog(MPost2Catalog):
    def __init__(self):
        self.tab_post2catalog = g_Post2Tag
        self.tab_catalog = g_Tag
        self.tab_post = g_Post

        try:
            g_Post2Tag.create_table()
        except:
            pass
