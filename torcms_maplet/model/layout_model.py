# -*- coding:utf-8 -*-

'''
Model for map layout.
'''
from torcms.core import tools
from torcms.model.abc_model import Mabc, MHelper
from torcms_maplet.model.map_tab import MabLayout


class MLayout(Mabc):
    '''
    Model for map layout.
    '''

    def __init__(self):
        super(MLayout, self).__init__()

    @staticmethod
    def get_by_uid(uid):
        '''
        :param uid:
        :return:
        '''
        return MHelper.get_by_uid(MabLayout, uid)

    @staticmethod
    def delete(uid):
        '''
        :param uid:
        :return:
        '''
        return MHelper.delete(MabLayout, uid)

    @staticmethod
    def query_by_app(app_id, user_id):
        '''
        :param app_id:
        :param user_id:
        :return:
        '''
        return MabLayout.select().where(
            (MabLayout.post_id == app_id) & (MabLayout.user_id == user_id)
        ).order_by(
            MabLayout.time_update.desc()
        )

    @staticmethod
    def add_or_update(post_data):
        '''
        :param post_data:
        :return:
        '''

        MabLayout.create(
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
