# -*- coding:utf-8 -*-

'''
Model for Evaluation
'''
from torcms.core import tools
from torcms.model.core_tab import g_Evaluation
from torcms.model.abc_model import Mabc

class MEvaluation(Mabc):
    def __init__(self):
        try:
            g_Evaluation.create_table()
        except:
            pass

    @staticmethod
    def app_evaluation_count(app_id, value=1):
        '''
        Get the Evalution sum.
        :param app_id:
        :param value:
        :return:
        '''
        return g_Evaluation.select().where(
            (g_Evaluation.post == app_id) & (g_Evaluation.value == value)
        ).count()

    @staticmethod
    def get_by_signature(user_id, app_id):
        '''
        :param user_id:
        :param app_id:
        :return:
        '''
        try:
            return g_Evaluation.get(
                (g_Evaluation.user == user_id) & (g_Evaluation.post == app_id)
            )
        except:
            return None

    @staticmethod
    def add_or_update(user_id, app_id, value):
        '''
        :param user_id:
        :param app_id:
        :param value:
        :return:
        '''
        rec = MEvaluation.get_by_signature(user_id, app_id)
        if rec:
            entry = g_Evaluation.update(
                value=value,
            ).where(g_Evaluation.uid == rec.uid)
            entry.execute()
        else:
            g_Evaluation.create(
                uid=tools.get_uuid(),
                user=user_id,
                app=app_id,
                value=value,
            )
