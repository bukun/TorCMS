# -*- coding:utf-8 -*-
'''
Model for Posts.
'''

from torcms.model.category_model import MCategory
from torcms.model.core_tab import TabPost, TabPost2Tag, TabTag


class MCatalog():
    '''
    Model for catalog list.
    '''
    def __init__(self):
        super().__init__()

    @staticmethod
    def query_by_slug(slug):
        '''
        查询全部章节
        '''
        cat_rec = MCategory.get_by_slug(slug)
        if cat_rec:
            cat_id = cat_rec.uid
        else:
            return None

        if cat_id.endswith('00'):
            cat_con = TabPost2Tag.par_id == cat_id
        else:
            cat_con = TabPost2Tag.tag_id == cat_id

        recs = TabPost.select().join(
            TabPost2Tag,
            on=(TabPost.uid == TabPost2Tag.post_id)).where(cat_con).order_by(
                TabPost.time_update.desc())

        return recs

    @staticmethod
    def query_all():
        '''
        查询大类记录
        '''

        recs = TabTag.select().where(TabTag.uid.endswith('00')).order_by(
            TabTag.uid)
        return recs
