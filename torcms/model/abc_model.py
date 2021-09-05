# -*- coding:utf-8 -*-
'''
The Base of Model
'''


class MHelper():
    '''
    Common used function for most Model. Using Model as the first parameter.
    '''
    @staticmethod
    def get_by_uid(model, uid):
        recs = model.select().where(model.uid == uid)
        if recs.count() == 0:
            return None
        else:
            return recs.get()

    @staticmethod
    def delete(model, uid):
        entry = model.delete().where(model.uid == uid)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False
