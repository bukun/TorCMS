# -*- coding:utf-8 -*-
'''
Handle the usage of the info.
'''

import sqlite3
import time

from torcms.core.tools import ts_helper


class MAcces():
    '''
    Handle the usage of the info.
    '''

    @staticmethod
    def get_all():
        pass

    @staticmethod
    def add(post_id):
        '''
        Create the record.
        '''

        ts30d = ts_helper()[2]

        # 使用毫秒作为ID。
        millis = int(round(time.time() * 1000))

        db_file = './database/log_access.db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        try:
            cursor.execute(
                'CREATE TABLE TabAccess (uid BIGINT PRIMARY KEY NOT NULL ,'
                'post_id VARCHAR(5));')
        except Exception as err:
            print(repr(err))

        try:
            cursor.execute(
                'CREATE TABLE TabPost (post_id VARCHAR(5) PRIMARY KEY NOT NULL ,'
                'count_1d integer , count_7d integer, count_30d integer );')
        except Exception as err:
            print(repr(err))

        del_cmd = 'delete from TabAccess where uid < {}'.format(ts30d)
        print(del_cmd)
        cursor.execute(del_cmd)
        conn.commit()

        cursor.execute(
            "select * from TabPost where post_id = '{}'".format(post_id))
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
        except Exception as err:
            print(repr(err))

        conn.commit()


if __name__ == '__main__':
    pass
