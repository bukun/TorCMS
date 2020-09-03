# -*- coding: utf-8
'''
创建sqlite数据库
'''
import os
import sqlite3


def run_create_db():
    db_file = os.path.join(os.getcwd(), 'access.db')
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE TabAccess (uid BIGINT PRIMARY KEY NOT NULL ,'
                   'post_id VARCHAR(5));')


if __name__ == '__main__':
    run_create_db()
