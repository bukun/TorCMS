# -*- coding:utf-8 -*-

'''
Rating for post.
'''

import peewee
from torcms.core import tools
from torcms.model.core_tab import TabRating
from torcms.model.abc_model import Mabc


class MRating(Mabc):
    '''
    Rating for post.
    '''

    # def __init__(self):
    #     super(MRating, self).__init__()

    @staticmethod
    def query_by_post(postid, limit=20):
        return TabRating.select().where(TabRating.post_id == postid).limit(limit)

    @staticmethod
    def query_average_rating(postid, limit=1000):
        return TabRating.select(
            peewee.fn.Avg(TabRating.rating).over(order_by=[TabRating.timestamp.desc()])
        ).where(
            TabRating.post_id == postid
        ).limit(limit).scalar()

    @staticmethod
    def get_rating(postid, userid):
        '''
        Get the rating of certain post and user.
        '''
        try:
            recs = TabRating.select().where(
                (TabRating.post_id == postid) & (TabRating.user_id == userid)
            )
        except:
            return False
        if recs.count() > 0:
            return recs.get().rating
        else:
            return False

    @staticmethod
    def update(postid, userid, rating):
        '''
        Update the rating of certain post and user.
        The record will be created if no record exists.
        '''
        rating_recs = TabRating.select().where(
            (TabRating.post_id == postid) & (TabRating.user_id == userid)
        )
        if rating_recs.count() > 0:
            MRating.__update_rating(rating_recs.get().uid, rating)
        else:
            MRating.__insert_data(postid, userid, rating)

    @staticmethod
    def __update_rating(uid, rating):
        '''
        Update rating.
        '''
        entry = TabRating.update(
            rating=rating
        ).where(TabRating.uid == uid)
        entry.execute()

    @staticmethod
    def __insert_data(postid, userid, rating):
        '''
        Inert new record.
        '''
        uid = tools.get_uuid()
        TabRating.create(
            uid=uid,
            post_id=postid,
            user_id=userid,
            rating=rating,
            timestamp=tools.timestamp(),
        )
        return uid
