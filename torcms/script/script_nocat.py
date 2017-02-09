# -*- coding:utf-8 -*-


from torcms.model.post_model import MPost
from torcms.model.post2catalog_model import MPost2Catalog
from config import router_post


def run_nocat():
    for key in router_post.keys():
        if key == 'i':
            continue
        post_recs = MPost.query_all(limit=50000, kind=key)
        for postinfo in post_recs:
            cat = MPost2Catalog.get_entry_catalog(postinfo.uid)
            if cat:
                pass
            else:
                print(postinfo.uid)
