# -*- coding:utf-8 -*-

from torcms.core.base_handler import BaseHandler
from torcms.model.rating_model import MRating
from torcms.model.post_model import MPost

from torcms.core.tools import logger


class RatingHandler(BaseHandler):
    def initialize(self):
        super(RatingHandler, self).initialize()
        self.mpost = MPost()
        self.mrating = MRating()

    def post(self, url_str=''):

        url_arr = self.parse_url(url_str)
        if len(url_arr) == 2 and url_arr[0] == '_update':
            self.update_rating(url_arr[1])
        elif len(url_arr) == 2 and url_arr[0] == '_updatepost':
            self.update_post(url_arr[1])

    def update_post(self, postid):
        uu = self.mrating.query_by_post(postid)
        if uu.count() > 10:
            rating = self.mrating.query_average_rating(postid)
        else:
            rating = 5

        logger.info('Get post rating: {rating}'.format(rating = rating))
        self.mpost.update_rating(postid, rating)

    def update_rating(self, postid):
        post_data = self.get_post_data()
        rating = float(post_data['rating'])
        postinfo = self.mpost.get_by_uid(postid)
        if postinfo and self.userinfo:
            self.mrating.update(postinfo.uid, self.userinfo.uid, rating=rating)
        else:
            return False
