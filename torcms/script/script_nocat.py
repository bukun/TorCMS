# -*- coding:utf-8 -*-

from torcms.model.info_model import MInfor
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.wiki_model import MWiki
from torcms.model.label_model import MLabel
from torcms.model.category_model import MCategory
from config import router_post

mcat = MCategory()
mlabel = MLabel()
mpost = MInfor()
mpost2tag = MPost2Catalog()
mwiki = MWiki()


def run_nocat():
    for key in router_post.keys():
        if key == 'i':
            continue
        post_recs = mpost.query_all(limit_num=50000, kind=key)
        for postinfo in post_recs:
            cat = mpost2tag.get_entry_catalog(postinfo.uid)
            if cat:
                pass
            else:
                print (postinfo.uid)

