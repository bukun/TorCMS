
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost

all_post2tag_recs = MPost2Catalog.just_query_all()

for post2tag_rec in all_post2tag_recs:
    post_id = post2tag_rec.post_id
    tag_id  = post2tag_rec.tag_id
    test_select = MPost.get_by_uid(post_id)
    if test_select:
        pass
    else:
        print(post_id)
        MPost2Catalog.del_by_uid(post2tag_rec.uid)