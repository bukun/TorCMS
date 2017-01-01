# -*- coding:utf-8 -*-


from torcms.core import tools
from torcms.model.core_tab import g_PostHist
from torcms.model.supertable_model import MSuperTable


class MInfoHist(MSuperTable):
    def __init__(self):
        self.tab = g_PostHist
        try:
            g_PostHist.create_table()
        except:
            pass

    def insert_data(self, raw_data):
        uid = tools.get_uuid()
        g_PostHist.create(
                uid=uid,
            post_id = raw_data.uid,
                title=raw_data.title,
                keywords = raw_data.keywords,
                user_name = raw_data.user_name,
                logo = raw_data.logo,
                date = raw_data.date,
                time_update = raw_data.time_update,
                cnt_md = raw_data.cnt_md,
                app_id = raw_data.uid,
                valid = raw_data.valid,
                extinfo = raw_data.extinfo,
            )
        return True
