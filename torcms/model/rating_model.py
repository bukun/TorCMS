# -*- coding:utf-8 -*-


import datetime

import tornado.escape
import peewee
from torcms.core import tools
from torcms.model.core_tab import g_Rating
from torcms.model.supertable_model import MSuperTable


class MRating(MSuperTable):
    def __init__(self):
        self.tab = g_Rating
        try:
            self.tab.create_table()
        except:
            pass

    def query_by_post(self, postid, limit=20):
        return self.tab.select().where(self.tab.post_id == postid).limit(limit)

    def query_average_rating(self, postid, limit=1000):
        return self.tab.select(peewee.fn.Avg(self.tab.rating).over(order_by=[self.tab.timestamp.desc()])).where(
            self.tab.post_id == postid).limit(limit).scalar()

    def get_rating(self, postid, userid):
        try:
            uu = self.tab.select().where((self.tab.post_id == postid) & (self.tab.user_id == userid))
        except:
            return False
        if uu.count() > 0:
            return uu.get().rating
        else:
            return False

    def update(self, postid, userid, rating):
        uu = self.tab.select().where((self.tab.post_id == postid) & (self.tab.user_id == userid))
        if uu.count() > 0:
            self.__update_rating(uu.get().uid, rating)
        else:
            self.__insert_data(postid, userid, rating)

    def __update_rating(self, uid, rating):
        print('update rating:', rating)
        entry = self.tab.update(
            rating=rating
        ).where(self.tab.uid == uid)
        entry.execute()

    def __insert_data(self, postid, userid, rating):
        uid = tools.get_uuid()
        self.tab.create(
            uid=uid,
            post_id=postid,
            user_id=userid,
            rating=rating,
            timestamp=tools.timestamp(),
        )
        return (uid)
