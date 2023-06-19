from pprint import pprint
import copy
from torcms.model.post_model import MPost

from config import post_cfg


def test_updata_extinfo_tag():
    for key in post_cfg.keys():
        print("*" * 50)
        print(key)

        recs = MPost.query_all(kind=key, limit=999999)

        for rec in recs:
            print('=' * 40)
            pprint(rec.extinfo)
            rec_extinfo = copy.deepcopy(rec.extinfo)
            upp = False
            for key in rec.extinfo:

                if key.startswith('tag_'):
                    # print(key, rec_extinfo[key])
                    new_key = '_' + key
                    if new_key in rec_extinfo:
                        pass
                    else:
                        upp = True
                        rec_extinfo[new_key] = rec_extinfo[key]

            if upp:
                pprint(rec_extinfo)
                # pass
                MPost.update_jsonb(rec.uid, rec_extinfo)
