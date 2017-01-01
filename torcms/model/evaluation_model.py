# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.core_tab import g_Post, g_Evaluation


class MEvaluation(object):
    def __init__(self):
        self.tab = g_Evaluation
        try:
            g_Evaluation.create_table()
        except:
            pass

    def query_recent(self, num = 10):
        return self.tab.select().join(g_Post).order_by(self.tab.timestamp.desc()).limit(num)

    def query_most(self, num):
        return self.tab.select().order_by(self.tab.count.desc()).limit(num)

    def app_evaluation_count(self, app_id, value = 1):
        return self.tab.select().where((self.tab.post == app_id) & (self.tab.value == value)).count()

    def get_by_signature(self, user_id, app_id):
        try:
            return self.tab.get((self.tab.user==user_id) & (self.tab.post == app_id))
        except:
            return False

    def add_or_update(self, user_id, app_id, value):
        if self.get_by_signature(user_id, app_id):
            tt = self.get_by_signature(user_id, app_id)
            entry = self.tab.update(
                value = value,
            ).where(self.tab.uid == tt.uid)
            entry.execute()
        else:
            entry = self.tab.create(
                uid = tools.get_uuid(),
                user = user_id,
                app  = app_id,
                value=value,
            )

    def delete_by_app_uid(self, uid):
        entry = self.tab.delete().where(self.tab.post == uid)
        uu = entry.execute()
