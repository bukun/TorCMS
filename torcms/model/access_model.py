# -*- coding:utf-8 -*-

'''
Handle the usage of the info.
'''

import time

from torcms.model.core_tab import TabAccess

from torcms.model.abc_model import Mabc


class MAcces(Mabc):
    '''
    Handle the usage of the info.
    '''

    @staticmethod
    def get_all():
        pass
        #
        # return TabAccess.select().order_by('timestamp').limit(10)

    #

    @staticmethod
    def add(post_id):
        '''
        Create the record.
        '''

        # 使用毫秒作为ID。
        millis = int(round(time.time() * 1000))

        # 有可能会冲突。由于只访问的记录，并不重要，所以直接跳过去。
        try:
            TabAccess.create(
                uid=millis,
                post_id=post_id,
            )
        except:
            pass
