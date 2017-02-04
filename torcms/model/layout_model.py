# -*- coding:utf-8 -*-

'''
Model for map layout.
'''
from torcms.core import tools
from torcms.model.map_tab import e_Layout
from torcms.model.abc_model import Mabc

class MLayout(Mabc):
    '''
    Model for map layout.
    '''

    def __init__(self):
        try:
            e_Layout.create_table()
        except:
            pass

    @staticmethod
    def get_by_id(uid):
        '''
        :param uid:
        :return:
        '''
        try:
            return e_Layout.get(e_Layout.uid == uid)
        except:
            return False

    @staticmethod
    def delete_by_uid(uid):
        '''
        :param uid:
        :return:
        '''
        qry = e_Layout.delete().where(e_Layout.uid == uid)
        try:
            qry.execute()
        except:
            return False

    @staticmethod
    def query_by_app(app_id, user_id):
        '''
        :param app_id:
        :param user_id:
        :return:
        '''
        return e_Layout.select().where(
            (e_Layout.post_id == app_id) & (e_Layout.user_id == user_id)
        ).order_by(
            e_Layout.time_update.desc()
        )

    @staticmethod
    def add_or_update(post_data):
        '''
        :param post_data:
        :return:
        '''
        print(post_data)
        e_Layout.create(
            uid=tools.get_uu8d(),
            title='',
            post_id=post_data['map'],
            user_id=post_data['user'],
            json=post_data['geojson'] if 'geojson' in post_data else '',
            lon=float(post_data['lon']),
            lat=float(post_data['lat']),
            zoom=int(post_data['zoom']),
            marker=int(post_data['marker']) if 'marker' in post_data else 0,
            time_create=tools.timestamp(),
            time_update=tools.timestamp(),
            public=1,
        )
