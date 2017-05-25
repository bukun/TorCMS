# -*- coding:utf-8 -*-

'''
For GeoJson storage.
'''
from torcms.core import tools
from torcms.model.abc_model import Mabc
from torcms_maplet.model.map_tab import MabGson, MabPost2Gson


class MPost2Gson(Mabc):

    @staticmethod
    def query_by_post(postid):
        '''
        Query records by post.
        :param postid:
        :return:
        '''
        return MabPost2Gson.select().where(
            MabPost2Gson.post_id == postid
        )


    @staticmethod
    def update_field(uid, post_id=None):
        if post_id:
            entry = MabPost2Gson.update(
                post_id=post_id
            ).where(MabPost2Gson.uid == uid)
            entry.execute()


class MJson(Mabc):
    '''
    For GeoJson storage.
    '''


    @staticmethod
    def get_by_id(uid):
        return MJson.get_by_uid(uid)

    @staticmethod
    def get_by_uid(uid):
        try:
            return MabGson.get(MabGson.uid == uid)
        except:
            return None

    @staticmethod
    def query_recent(user_id, num=10):
        return MabGson.select().where(
            MabGson.user_id == user_id
        ).order_by(
            MabGson.time_update.desc()
        ).limit(num)

    @staticmethod
    def query_by_app(app_id, user_id):
        return MabGson.select().join(MabPost2Gson, on=(MabPost2Gson.json_id == MabGson.uid)).where(
            (MabPost2Gson.post_id == app_id) &
            (MabGson.user_id == user_id)
        ).order_by(
            MabGson.time_update.desc()
        )

    @staticmethod
    def delete_by_uid(uid):
        entry = MabGson.delete().where(MabGson.uid == uid)
        try:
            entry.execute()
            return True
        except:
            return False

    @staticmethod
    def add_or_update_json(json_uid, user_id, geojson):
        current_count = MabGson.select().where(
            MabGson.uid == json_uid
        ).count()

        if current_count > 0:
            cur_record = MJson.get_by_uid(json_uid)
            entry = MabGson.update(
                json=geojson,
                time_update=tools.timestamp(),
            ).where(MabGson.uid == cur_record.uid)
            entry.execute()

        else:
            MabGson.create(uid=json_uid,
                           title='',
                           user_id=user_id,
                           json=geojson,
                           time_create=tools.timestamp(),
                           time_update=tools.timestamp(),
                           public=1)

    @staticmethod
    def add_or_update(json_uid, user_id, app_id, geojson):
        current_count = MabGson.select().where(
            MabGson.uid == json_uid
        ).count()
        MJson.add_or_update_json(json_uid, user_id, geojson)

        if current_count:
            pass
        else:
            MabPost2Gson.create(uid=tools.get_uuid(),
                                post_id=app_id,
                                json_id=json_uid)
