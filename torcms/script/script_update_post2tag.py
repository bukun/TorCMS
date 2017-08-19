# -*- coding:utf-8 -*-


from torcms.model.post2catalog_model import MPost2Catalog


def run_update_cat(*args):
    recs = MPost2Catalog.query_all().naive()
    for rec in recs:
        if rec.tag_kind != 'z':
            print('-' * 40)
            print(rec.uid)
            print(rec.tag_id)
            print(rec.par_id)

            MPost2Catalog.update_field(rec.uid, par_id=rec.tag_id[:2] + "00")
