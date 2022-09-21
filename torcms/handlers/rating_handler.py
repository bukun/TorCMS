# -*- coding:utf-8 -*-
'''
For rating.
'''

import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.core.tools import logger
from torcms.model.post_model import MPost
from torcms.model.rating_model import MRating


class RatingHandler(BaseHandler):
    '''
    For rating.

    评分处理
    '''

    def initialize(self, **kwargs):
        super().initialize()

    def post(self, *args, **kwargs):

        url_str = args[0]

        url_arr = self.parse_url(url_str)
        if len(url_arr) == 2 and url_arr[0] == '_update':
            self.update_rating(url_arr[1])
        elif len(url_arr) == 2 and url_arr[0] == '_updatepost':
            # Shouldn't be called via http.
            self.update_post(url_arr[1])

    def update_post(self, postid):
        '''
        The rating of Post should be updaed if the count is greater than 10


        '''
        voted_recs = MRating.query_by_post(postid)
        if voted_recs.count() > 10:
            rating = MRating.query_average_rating(postid)
        else:
            rating = 5

        logger.info('Get post rating: {rating}'.format(rating=rating))
        # MPost.__update_rating(postid, rating)
        MPost.update_misc(postid, rating=rating)

    @tornado.web.authenticated
    def update_rating(self, postid):
        '''
        only the used who logged in would voting.
        '''
        post_data = self.get_request_arguments()
        rating = float(post_data['rating'])
        postinfo = MPost.get_by_uid(postid)
        if postinfo and self.userinfo:
            MRating.update(postinfo.uid, self.userinfo.uid, rating=rating)
            self.update_post(postid)
        else:
            return False
