# -*- coding:utf-8 -*-

import peewee
from torcms.core import tools
from torcms.model.core_tab import g_Rating
from torcms.model.abc_model import Mabc

class MRating(Mabc):
    def __init__(self):
        try:
            g_Rating.create_table()
        except:
            pass

    @staticmethod
    def query_by_post(postid, limit=20):
        return g_Rating.select().where(g_Rating.post_id == postid).limit(limit)

    @staticmethod
    def query_average_rating(postid, limit=1000):
        return g_Rating.select(
            peewee.fn.Avg(g_Rating.rating).over(order_by=[g_Rating.timestamp.desc()])
        ).where(
            g_Rating.post_id == postid
        ).limit(limit).scalar()

    @staticmethod
    def get_rating(postid, userid):
        try:
            uu = g_Rating.select().where((g_Rating.post_id == postid) & (g_Rating.user_id == userid))
        except:
            return False
        if uu.count() > 0:
            return uu.get().rating
        else:
            return False

    @staticmethod
    def update(postid, userid, rating):
        uu = g_Rating.select().where((g_Rating.post_id == postid) & (g_Rating.user_id == userid))
        if uu.count() > 0:
            MRating.__update_rating(uu.get().uid, rating)
        else:
            MRating.__insert_data(postid, userid, rating)

    @staticmethod
    def __update_rating(uid, rating):
        print('update rating:', rating)
        entry = g_Rating.update(
            rating=rating
        ).where(g_Rating.uid == uid)
        entry.execute()

    @staticmethod
    def __insert_data(postid, userid, rating):
        uid = tools.get_uuid()
        g_Rating.create(
            uid=uid,
            post_id=postid,
            user_id=userid,
            rating=rating,
            timestamp=tools.timestamp(),
        )
        return uid
