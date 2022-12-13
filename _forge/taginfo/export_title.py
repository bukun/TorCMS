# -*- coding:utf-8 -*-
'''
将 OSGeo 数据库中的 Posts 导出。
'''

import os
import sys

sys.path.append('.')

from torcms.model.post_model import MPost
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog

import re

from config import router_post

out_ws = 'xx_title'


def get_img(text):
    pattern = re.compile('!\[.*?\]\(.*?\)')
    # pattern = re.compile('''(?|(?<txt>(?<url>(?:ht|f)tps?://\S+(?<=\P{P})))|\(([^)]+)\)\[(\g<url>)\])''')
    tt = re.findall(pattern, text)
    for t in tt:
        print('>' * 40)
        print(t, t.strip(')').split('(')[-1])
        print('<' * 40)
    return tt


def do_for_cat(rec):
    kind = rec.kind
    pid = rec.pid
    cat_id = rec.uid

    out_base_dir = os.path.join(out_ws, kind, pid)
    print(out_base_dir)
    if os.path.exists(out_base_dir):
        pass
    else:
        os.makedirs(out_base_dir)

    post2tag_recs = MPost2Catalog.query_by_catid(cat_id)

    out_file = os.path.join(out_base_dir, cat_id + '.md')

    with open(out_file, 'w') as fout_md:

        for post2tag_rec in post2tag_recs:
            # print(post2tag_rec.post_id)
            postinfo = MPost.get_by_uid(post2tag_rec.post_id)
            fout_md.write('{}|{}\n'.format(postinfo.uid, postinfo.title))


def run_export():
    for kind in router_post:
        # print(router)
        all_cats = MCategory.query_all(kind)
        for rec in all_cats:
            print(rec.uid, rec.pid)
            if rec.pid == '0000':
                continue

            else:
                do_for_cat(rec)


if __name__ == '__main__':
    run_export()
