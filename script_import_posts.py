import os

from torcms.model.post_model import MPost
from torcms.model.post2catalog_model import MPost2Catalog
import yaml

filter_arr = []
with open('xx_diff_map.list', 'r') as fii:
    for x in fii.readlines():
        x = x.strip()
        if x:
            filter_arr.append(x)

print(filter_arr)

yaml_infos = yaml.load(open('xx_posts.yaml'))


def run_export():
    for x in yaml_infos:

        if x['uid'] in filter_arr:

            print(x['uid'])
            MPost.create_post(x['uid'], x)

            x['extinfo']['def_cat_uid'] = x['extinfo'].get('def_cat_uid', '2103')

            print(x['extinfo']['def_cat_uid'])

            if x['extinfo']['def_cat_uid'] in ['me01', 'me02', 'mf01', 'mf03']:
                # pass
                MPost2Catalog.add_record(x['uid'], x['extinfo']['def_cat_uid'])
            else:
                # pass
                MPost2Catalog.add_record(x['uid'], '2103')

        pass
    # all_recs = MPost.query_all(kind='1', limit=10000)
    # out_arr = []
    # for postinfo in all_recs:
    #     out_arr.append(
    #         {
    #             'uid': postinfo.uid,
    #             'title': postinfo.title,
    #             'keywords': postinfo.keywords,
    #             'date': postinfo.date,
    #             'extinfo': postinfo.extinfo,
    #             'cnt_md': postinfo.cnt_md,
    #             'cnt_html': postinfo.cnt_html,
    #             'kind': postinfo.kind,
    #         }
    #     )
    #
    # dumper = ruamel.yaml.RoundTripDumper
    #
    # with open('xx_posts.yaml', 'w') as fo:
    #     yaml.dump(out_arr, fo, Dumper=dumper, allow_unicode=True)


if __name__ == '__main__':
    run_export()
