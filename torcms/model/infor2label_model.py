# -*- coding:utf-8 -*-

import config
from torcms.model.core_tab import g_Post
from torcms.model.core_tab import g_Tag
from torcms.model.core_tab import g_Post2Tag
from torcms.model.label_model import MLabel
from torcms.model.label_model import MPost2Label


class MInforLabel(MLabel):
    def __init__(self):
        self.tab = g_Tag
        self.tab2 = g_Post2Tag


class MInfor2Label(MPost2Label):
    def __init__(self):
        self.tab = g_Post2Tag
        self.tab_label = g_Tag
        self.tab_post = g_Post
        self.mtag = MInforLabel()
        try:
            g_Post2Tag.create_table()
        except:
            pass

    def query_count(self, uid):
        return self.tab.select().where(self.tab.tag == uid).count()
