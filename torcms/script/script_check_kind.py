# -*- coding:utf-8 -*-

from torcms.model.post_model import MPost
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.category_model import MCategory
from config import router_post


def run_check_kind(*args):
    for kd in router_post.keys():
        for rec in MCategory.query_all(kind=kd):
            catid = rec.uid

            catinfo = MCategory.get_by_uid(catid)
            recs = MPost2Catalog.query_by_catid(catid)
            for rec in recs:
                postinfo = MPost.get_by_uid(rec.post_id)
                if postinfo.kind == catinfo.kind:
                    pass
                else:
                    print(postinfo.uid)
