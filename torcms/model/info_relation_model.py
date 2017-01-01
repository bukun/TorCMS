# -*- coding:utf-8 -*-

from torcms.model.core_tab import  g_Rel, g_Post
from torcms.model.relation_model import MRelation
from torcms.model.core_tab import g_Post2Tag

from torcms.model.infor2catalog_model import MInfor2Catalog


class MInforRel(MRelation):
    def __init__(self):
        self.tab_relation = g_Rel
        self.tab_post = g_Post
        self.tab_post2tag = g_Post2Tag

        self.minfo2tag = MInfor2Catalog()
        try:
            g_Rel.create_table()
        except:
            pass


class MRelPost2Infor(MRelation):
    def __init__(self):
        MRelation.__init__(self)
        self.tab_relation = g_Rel
        self.tab_post = g_Post
        try:
            self.tab_relation.create_table()
        except:
            pass


class MRelInfor2Post(MRelation):
    def __init__(self):
        MRelation.__init__(self)
        self.tab_relation = g_Rel
        self.tab_post = g_Post
        try:
            self.tab_relation.create_table()
        except:
            pass
