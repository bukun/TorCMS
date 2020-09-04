# -*- coding:utf-8 -*-

'''
Handle the usage of the info.
'''

import time
import os
import sqlite3
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

        db_file = os.path.join(os.getcwd(), 'access.db')
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        try:
            cursor.execute('CREATE TABLE TabAccess (uid BIGINT PRIMARY KEY NOT NULL ,'
                           'post_id VARCHAR(5));')
        except:
            pass

        try:
            sql = '''insert into TabAccess (uid, post_id) values (?,?)'''
            para = (millis, post_id)
            cursor.execute(sql, para)
            conn.commit()
        except:
            pass

        cursor.execute('SELECT * FROM TabAccess;')

        conn.commit()

        print("2" * 50)
        print(cursor.fetchall())



        # 有可能会冲突。由于只访问的记录，并不重要，所以直接跳过去。
        # try:
        #     TabAccess.create(
        #         uid=millis,
        #         post_id=post_id,
        #     )
        # except:
        #     pass
