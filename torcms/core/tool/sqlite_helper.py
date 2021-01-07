# -*- coding:utf-8 -*-

'''
Handle the usage of the info.
'''

import time
import os
import sqlite3

from torcms.core.tools import ts_helper

# from torcms.model.core_tab import TabAccess

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

        ts1d, ts7d, ts30d = ts_helper()


        # 使用毫秒作为ID。
        millis = int(round(time.time() * 1000))

        db_file = './database/log_access.db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()



        try:
            cursor.execute('CREATE TABLE TabAccess (uid BIGINT PRIMARY KEY NOT NULL ,'
                           'post_id VARCHAR(5));')
        except:
            pass

        try:
            cursor.execute('CREATE TABLE TabPost (post_id VARCHAR(5) PRIMARY KEY NOT NULL ,'
                           'count_1d integer , count_7d integer, count_30d integer );')
        except:
            pass

        del_cmd = 'delete from TabAccess where uid < {}'.format(ts30d)
        print(del_cmd)
        cursor.execute(del_cmd)
        conn.commit()

        cursor.execute("select * from TabPost where post_id = '{}'".format(post_id))
        rec = cursor.fetchone()
        print(rec)
        if rec:
            pass
        else:
            sql = 'insert into TabPost (post_id, count_1d, count_7d, count_30d) values (?,?, ?, ?)'
            para = (post_id, 1, 1, 1)
            cursor.execute(sql, para)

        try:
            sql = '''insert into TabAccess (uid, post_id) values (?,?)'''
            para = (millis, post_id)
            cursor.execute(sql, para)
        except:
            pass

        conn.commit()



        # cursor.execute('SELECT * FROM TabAccess;')
        # conn.commit()

        # print("2" * 50)
        # print(cursor.fetchall())

        # 有可能会冲突。由于只访问的记录，并不重要，所以直接跳过去。
        # try:
        #     TabAccess.create(
        #         uid=millis,
        #         post_id=post_id,
        #     )
        # except:
        #     pass


if __name__ == '__main__':
    MAcces.add('145db')
