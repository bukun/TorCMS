# -*- coding:utf-8 -*-

'''
Model for Evaluation
'''
from torcms.core import tools
from torcms.model.core_tab import g_Evaluation


class MEvaluation(object):
    def __init__(self):
        self.tab = g_Evaluation
        try:
            g_Evaluation.create_table()
        except:
            pass

    def app_evaluation_count(self, app_id, value=1):
        '''
        Get the Evalution sum.
        :param app_id:
        :param value:
        :return:
        '''
        return self.tab.select().where(
            (self.tab.post == app_id) & (self.tab.value == value)
        ).count()

    def get_by_signature(self, user_id, app_id):
        '''
        :param user_id:
        :param app_id:
        :return:
        '''
        try:
            return self.tab.get(
                (self.tab.user == user_id) & (self.tab.post == app_id)
            )
        except:
            return None

    def add_or_update(self, user_id, app_id, value):
        '''
        :param user_id:
        :param app_id:
        :param value:
        :return:
        '''
        rec = self.get_by_signature(user_id, app_id)
        if rec:
            entry = self.tab.update(
                value=value,
            ).where(self.tab.uid == rec.uid)
            entry.execute()
        else:
            self.tab.create(
                uid=tools.get_uuid(),
                user=user_id,
                app=app_id,
                value=value,
            )

    def delete_by_app_uid(self, uid):
        entry = self.tab.delete().where(self.tab.post == uid)
        entry.execute()
