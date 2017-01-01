#


import time
from datetime import datetime

import config
from config import cfg
import peewee
from torcms.core import tools
from torcms.model.supertable_model import MSuperTable
from torcms.model.core_tab import g_Post
from torcms.model.core_tab import g_Post2Tag
from torcms.model.core_tab import g_Post2Tag as CabPost2Label
from torcms.model.core_tab import g_Usage
from torcms.model.core_tab import g_Rel
from torcms.model.core_tab import g_Reply


from torcms.model.info_model import MInfor

class MInfor(MInfor):
    def __init__(self):
        self.kind = 'm'
        self.tab = g_Post
        self.tab_app = g_Post
        self.tab_app2catalog = g_Post2Tag
        self.tab_relation = g_Rel
        self.tab_app2label = CabPost2Label
        self.tab_usage = g_Usage
        self.cab_reply = g_Reply
        try:
            g_Post.create_table()
        except:
            pass

