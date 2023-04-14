# -*- coding:utf-8 -*-
'''
The Base of Model
'''


class MHelper:
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

    @staticmethod
    def query_all_parger(model, current_page_num, perPage):

        return model.select().paginate(current_page_num, perPage)

    @staticmethod
    def get_counts(model):
        '''
        The count in table.
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        return model.select().count(None)
