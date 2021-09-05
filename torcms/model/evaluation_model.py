# -*- coding:utf-8 -*-
'''
Model for Evaluation
'''
from torcms.core import tools
from torcms.model.core_tab import TabEvaluation


class MEvaluation():
    '''
    Model for Evaluation
    '''
    @staticmethod
    def app_evaluation_count(app_id, value=1):
        '''
        Get the Evalution sum.
        '''
        return TabEvaluation.select().where(
            (TabEvaluation.post_id == app_id)
            & (TabEvaluation.value == value)).count()

    @staticmethod
    def get_by_signature(user_id, app_id):
        '''
        get by user ID, and app ID.
        '''
        try:
            return TabEvaluation.get((TabEvaluation.user_id == user_id)
                                     & (TabEvaluation.post_id == app_id))
        except Exception as err:
            print(repr(err))
            return None

    @staticmethod
    def add_or_update(user_id, app_id, value):
        '''
        Editing evaluation.
        '''
        rec = MEvaluation.get_by_signature(user_id, app_id)
        if rec:
            entry = TabEvaluation.update(
                value=value, ).where(TabEvaluation.uid == rec.uid)
            entry.execute()
        else:
            TabEvaluation.create(
                uid=tools.get_uuid(),
                user_id=user_id,
                post_id=app_id,
                value=value,
            )
