# -*- coding: utf-8

import sys
from config import router_post
from torcms.model.category_model import MCategory

# from torcms.model.infor2catalog_model import MInfor2Catalog
from torcms.model.post2catalog_model import MPost2Catalog

def run_update_count():
    mapp2cat = MPost2Catalog()
    mappcat = MCategory()

    for kd in router_post.keys():
        for rec in mappcat.query_all(kind=kd):
            uid = rec.uid
            uuvv = mapp2cat.query_by_catid(rec.uid)
            mappcat.update_count(uid, uuvv.count())
