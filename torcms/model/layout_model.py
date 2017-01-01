# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.map_tab import *


class MLayout(object):
    def __init__(self):
        try:
            e_Layout.create_table()
        except:
            pass

    def get_by_id(self, uid):
        try:
            return e_Layout.get(e_Layout.uid == uid)
        except:
            return False

    def delete_by_uid(self, uid):
        q = e_Layout.delete().where(e_Layout.uid == uid)
        try:
            q.execute()
        except:
            return False
        
    def query_recent(self, user_id, num=10):
        return e_Layout.select().where(e_Layout.user == user_id).order_by(e_Layout.order).limit(num)

    def query_by_app(self, app_id, user_id):
        return e_Layout.select().where((e_Layout.post_id == app_id) & (e_Layout.user_id == user_id)).order_by(
            e_Layout.time_update.desc())

    def add_or_update(self, post_data):
        print(post_data)
        entry = e_Layout.create(
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
        print(entry)
