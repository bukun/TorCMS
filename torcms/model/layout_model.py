# -*- coding:utf-8 -*-

'''
Model for map layout.
'''
from torcms.core import tools
from torcms.model.map_tab import e_Layout


class MLayout(object):
    '''
    Model for map layout.
    '''

    def __init__(self):
        self.tab = e_Layout
        try:
            self.tab.create_table()
        except:
            pass

    def get_by_id(self, uid):
        '''
        :param uid:
        :return:
        '''
        try:
            return self.tab.get(self.tab.uid == uid)
        except:
            return False

    def delete_by_uid(self, uid):
        '''
        :param uid:
        :return:
        '''
        qry = self.tab.delete().where(self.tab.uid == uid)
        try:
            qry.execute()
        except:
            return False

    # def query_recent(self, user_id, num=10):
    #     return self.tab.select().where(self.tab.user == user_id
    # ).order_by(self.tab.order).limit(num)

    def query_by_app(self, app_id, user_id):
        '''
        :param app_id:
        :param user_id:
        :return:
        '''
        return self.tab.select().where(
            (self.tab.post_id == app_id) & (self.tab.user_id == user_id)
        ).order_by(
            self.tab.time_update.desc()
        )

    def add_or_update(self, post_data):
        '''
        :param post_data:
        :return:
        '''
        print(post_data)
        self.tab.create(
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
