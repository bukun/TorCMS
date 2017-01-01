# -*- coding: utf-8

import sys
from config import router_post
from torcms.model.category_model import MCategory

from torcms.model.infor2catalog_model import MInfor2Catalog
def run_update_count():
    mapp2cat = MInfor2Catalog()
    mappcat = MCategory()

    for kd in router_post.keys():
        for rec in mappcat.query_all( kind = kd ):
            uid= rec.uid
            print(rec.name)
            uuvv = mapp2cat.query_by_catid(rec.uid)
            print(uid, uuvv.count())
            mappcat.update_count(uid, uuvv.count())
