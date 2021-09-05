# -*- coding:utf-8 -*-
'''
Model for classify.
'''

from config import CMS_CFG
from torcms.model.core_tab import TabPost, TabPost2Tag, TabTag


class MClassify():
    '''
    Model for classify.
    '''
    def __init__(self):
        super().__init__()

    @staticmethod
    def query_pager_by_classify(current_page_num=1):
        recs = TabTag.select().where(TabTag.uid.endswith("00")).order_by(
            TabTag.uid).paginate(current_page_num, CMS_CFG['list_num'])

        return recs

    @staticmethod
    def count_of_certain():
        recs = TabTag.select().where(TabTag.uid.endswith("00"))
        return recs.count()

    @staticmethod
    def query_pager_by_classify_all():
        recs = TabTag.select().where(TabTag.uid.endswith("00")).order_by(
            TabTag.uid)

        return recs

    @staticmethod
    def count_of_classify(tagid):

        if tagid.endswith('00'):
            recs = TabPost.select().join(
                TabPost2Tag, on=(TabPost2Tag.post_id == TabPost.uid)).join(
                    TabTag, on=(TabPost2Tag.tag_id == TabTag.uid)).where(
                        TabTag.uid.startswith(tagid[:2]))
        else:
            recs = TabPost.select().join(
                TabPost2Tag, on=(TabPost2Tag.post_id == TabPost.uid)).join(
                    TabTag, on=(TabPost2Tag.tag_id == TabTag.uid)).where(
                        TabTag.uid == tagid)

        return recs.count()
