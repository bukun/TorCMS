# -*- coding:utf-8 -*-

'''
For GeoJson storage.
'''
from torcms.core import tools

# from torcms.model.abc_model import Mabc
from torcms.model.user_model import MUser
from torcms_maplet.model.map_tab import MabGson, MabPost2Gson


class MPost2Gson:
    def __init__(self):
        super(MPost2Gson, self).__init__()

        try:
            MabPost2Gson.create()
        except Exception:
            pass

    @staticmethod
    def query_by_post(postid):
        '''
        Query records by post.
        :param postid:
        :return:
        '''
        return MabPost2Gson.select().where(MabPost2Gson.post_id == postid)

    @staticmethod
    def update_field(uid, post_id=None):
        if post_id:
            entry = MabPost2Gson.update(post_id=post_id).where(MabPost2Gson.uid == uid)
            entry.execute()


class MJson:
    '''
    For GeoJson storage.
    '''

    def __init__(self):
        super(MJson, self).__init__()
        # Todo: should be deleted.
        try:
            MabGson.create()
        except Exception:
            pass

    @staticmethod
    def get_by_id(uid):
        return MJson.get_by_uid(uid)

    @staticmethod
    def get_by_uid(uid):
        try:
            return MabGson.get(MabGson.uid == uid)
        except Exception:
            return None

    @staticmethod
    def query_recent(user_id='', num=10):
        if user_id:
            recs = (
                MabGson.select()
                .where(MabGson.user_id == user_id)
                .order_by(MabGson.time_update.desc())
                .limit(num)
            )
        else:
            recs = MabGson.select().order_by(MabGson.time_update.desc()).limit(num)
        return recs

    @staticmethod
    def query_by_app(app_id, user_id):
        return (
            MabGson.select()
            .join(MabPost2Gson, on=(MabPost2Gson.json_id == MabGson.uid))
            .where((MabPost2Gson.post_id == app_id) & (MabGson.user_id == user_id))
            .order_by(MabGson.time_update.desc())
        )

    @staticmethod
    def delete_by_uid(uid):
        entry = MabGson.delete().where(MabGson.uid == uid)
        try:
            entry.execute()
            return True
        except Exception:
            return False

    @staticmethod
    def add_or_update_json(json_uid, user_id, geojson, post_data, version=0):
        if version:
            pass
        else:
            return False

        userinfo = MUser.get_by_uid(user_id)
        if userinfo:
            pass
        else:
            user_id = ''
        current_count = MabGson.select().where(MabGson.uid == json_uid).count()

        if current_count > 0:
            cur_record = MJson.get_by_uid(json_uid)
            entry = MabGson.update(
                title=post_data['title'],
                json=geojson,
                time_update=tools.timestamp(),
            ).where(MabGson.uid == cur_record.uid)
            entry.execute()

        else:
            MabGson.create(
                uid=json_uid,
                title='',
                user_id=user_id,
                json=geojson,
                time_create=tools.timestamp(),
                time_update=tools.timestamp(),
                version=version,
                public=1,
            )

    @staticmethod
    def add_or_update(json_uid, user_id, app_id, geojson, version=2):
        current_count = MabGson.select().where(MabGson.uid == json_uid).count()
        post_data = {'title': ''}
        MJson.add_or_update_json(json_uid, user_id, geojson, post_data, version=version)

        post2gson_rec = MabPost2Gson.select().where(
            (MabPost2Gson.post_id == app_id) & (MabPost2Gson.json_id == json_uid)
        )

        if post2gson_rec.count():
            pass
        else:
            MabPost2Gson.create(uid=tools.get_uuid(), post_id=app_id, json_id=json_uid)
