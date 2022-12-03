# -*- coding:utf-8 -*-

'''
地图日志
'''

import sqlite3
import os
from torcms.core import tools

'''
try:
   cursor.execute('CREATE TABLE TabMaplog (uid VARCHAR NOT NULL ,'
                           'lat VARCHAR,'
                           'lon VARCHAR,'
                           'center VARCHAR,'
                           'zoom VARCHAR,'
                           'zoom_min VARCHAR,'
                           'zoom_max VARCHAR,'
                           'geojson VARCHAR,'
                           'kind VARCHAR,'
                           'create_time INTEGER,'
                           'user_uid VARCHAR,'
                           'user_ip VARCHAR,'
                           'user_browser VARCHAR);')
except:
    pass
'''


class MMapLog():
    '''
    Handle the usage of the info.
    '''

    @staticmethod
    def get_all():
        pass

    @staticmethod
    def add(post_data):
        '''
        Create the record.
        '''

        db_file = os.path.join(os.getcwd(), 'xx_map_log.db')
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        try:
            cursor.execute('CREATE TABLE TabMaplog (uid VARCHAR NOT NULL ,'
                           'lat VARCHAR,'
                           'lon VARCHAR,'
                           'center VARCHAR,'
                           'zoom VARCHAR,'
                           'zoom_min VARCHAR,'
                           'zoom_max VARCHAR,'
                           'geojson VARCHAR,'
                           'kind VARCHAR,'
                           'create_time INTEGER,'
                           'user_uid VARCHAR,'
                           'user_ip VARCHAR,'
                           'user_browser VARCHAR);')
        except Exception:
            pass
        try:
            sql = '''insert into TabMaplog (uid,lat,lon,center,zoom,zoom_min,zoom_max,geojson,kind,create_time,user_uid,user_ip,user_browser) values (?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            para = (post_data['uid'], post_data['lat'], post_data['lon'], post_data['center'], post_data['zoom'],
                    post_data['zoom_min'], post_data['zoom_max'], post_data['geojson'], post_data['kind'],
                    tools.timestamp(), post_data['user'], post_data['user_ip'], post_data['browser'])

            cursor.execute(sql, para)
            conn.commit()
        except Exception:
            pass

    @staticmethod
    def get_all():
        db_file = os.path.join(os.getcwd(), 'xx_map_log.db')
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM TabMaplog ORDER BY create_time DESC;')
        recs = cursor.fetchall()
        return recs
