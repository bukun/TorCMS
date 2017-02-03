# -*- coding:utf-8 -*-


from torcms.core import tools
from torcms.model.core_tab import g_PostHist
from torcms.model.abc_model import Mabc


class MInfoHist(Mabc):
    def __init__(self):
        self.tab = g_PostHist
        try:
            g_PostHist.create_table()
        except:
            pass

    def create_wiki_history(self, post_data):
        uid = tools.get_uuid()
        g_PostHist.create(
                uid=uid,
            post_id = post_data.uid,
                title=post_data.title,
                keywords = post_data.keywords,
                user_name = post_data.user_name,
                logo = post_data.logo,
                date = post_data.date,
                time_update = post_data.time_update,
                cnt_md = post_data.cnt_md,
                app_id = post_data.uid,
                valid = post_data.valid,
                extinfo = post_data.extinfo,
            )
        return True
