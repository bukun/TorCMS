# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.map_tab import *


class MJson(object):
    def __init__(self):
        try:
            e_Json.create_table()
        except:
            pass
        try:
            e_Post2Json.create_table()
        except:
            pass

    def get_by_id(self, uid):
        try:
            return e_Json.get(e_Json.uid == uid)
        except:
            return False

    def query_recent(self, user_id, num=10):
        return e_Json.select().where(e_Json.user_id == user_id).order_by(e_Json.time_update.desc()).limit(num)

    def query_by_app(self, app_id, user_id):
        # return TabMap2Json.select().join(TabJson).where ( (TabMap2Json.app.uid == app_id) & (TabJson.user == user_id) ).order_by(TabJson.time_update.desc())
        return e_Json.select().join(e_Post2Json).where((e_Post2Json.post_id == app_id) & (e_Json.user_id == user_id)).order_by(
            e_Json.time_update.desc())


    def delete_by_uid(self, uid):
        q = e_Json.delete().where(e_Json.uid == uid)
        try:
            q.execute()
        except:
            return False

    def add_or_update_json(self, json_uid, user_id, geojson):
        current_count = e_Json.select().where(e_Json.uid == json_uid).count()

        if current_count > 0:
            cur_record = self.get_by_id(json_uid)
            entry = e_Json.update(
                json=geojson,
                time_update=tools.timestamp(),
            ).where(e_Json.uid == cur_record.uid)
            entry.execute()

        else:
            entry = e_Json.create(
                uid=json_uid,
                title='',
                # app=app_id,
                user_id=user_id,
                json=geojson,
                time_create=tools.timestamp(),
                time_update=tools.timestamp(),
                public=1,
            )
    def add_or_update(self, json_uid, user_id, app_id, geojson):
        print('create geojson: app_id,', app_id, '; json_uid,', json_uid)
        current_count = e_Json.select().where(e_Json.uid == json_uid).count()
        self.add_or_update_json(json_uid, user_id, geojson)

        if current_count:
            pass
        else:
            entry = e_Post2Json.create(
                uid = tools.get_uuid(),
                post_id = app_id,
                json = json_uid,
            )
