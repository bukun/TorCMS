# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.map_tab import *
from torcms.model.abc_model import Mabc

class MJson(Mabc):
    def __init__(self):
        try:
            e_Json.create_table()
        except:
            pass
        try:
            e_Post2Json.create_table()
        except:
            pass

    @staticmethod
    def get_by_id(uid):
        return MJson.get_by_uid(uid)

    @staticmethod
    def get_by_uid(uid):
        try:
            return e_Json.get(e_Json.uid == uid)
        except:
            return None

    @staticmethod
    def query_recent(user_id, num=10):
        return e_Json.select().where(
            e_Json.user_id == user_id
        ).order_by(
            e_Json.time_update.desc()
        ).limit(num)

    @staticmethod
    def query_by_app(app_id, user_id):
        return e_Json.select().join(e_Post2Json).where(
            (e_Post2Json.post_id == app_id) &
            (e_Json.user_id == user_id)
        ).order_by(
            e_Json.time_update.desc()
        )

    @staticmethod
    def delete_by_uid(uid):
        q = e_Json.delete().where(e_Json.uid == uid)
        try:
            q.execute()
        except:
            return False

    @staticmethod
    def add_or_update_json(json_uid, user_id, geojson):
        current_count = e_Json.select().where(
            e_Json.uid == json_uid
        ).count()

        if current_count > 0:
            cur_record = MJson.get_by_uid(json_uid)
            entry = e_Json.update(
                json=geojson,
                time_update=tools.timestamp(),
            ).where(e_Json.uid == cur_record.uid)
            entry.execute()

        else:
            e_Json.create(uid=json_uid,
                          title='',
                          user_id=user_id,
                          json=geojson,
                          time_create=tools.timestamp(),
                          time_update=tools.timestamp(),
                          public=1)

    @staticmethod
    def add_or_update(json_uid, user_id, app_id, geojson):
        current_count = e_Json.select().where(
            e_Json.uid == json_uid
        ).count()
        MJson.add_or_update_json(json_uid, user_id, geojson)

        if current_count:
            pass
        else:
            e_Post2Json.create(uid=tools.get_uuid(),
                               post_id=app_id,
                               json=json_uid)
