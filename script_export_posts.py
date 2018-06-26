import os

from torcms.model.post_model import MPost
import yaml
import ruamel.yaml


def run_export():
    all_recs = MPost.query_all(kind='m', limit=10000)
    out_arr = []
    for postinfo in all_recs:
        out_arr.append(
            {
                'uid': postinfo.uid,
                'title': postinfo.title,
                'keywords': postinfo.keywords,
                'date': postinfo.date,
                'extinfo': postinfo.extinfo,
                'cnt_md': postinfo.cnt_md,
                'cnt_html': postinfo.cnt_html,
                'kind': postinfo.kind,
                'user_name': postinfo.user_name,
                'logo': '',
            }
        )

    dumper = ruamel.yaml.RoundTripDumper

    with open('xx_posts.yaml', 'w') as fo:
        yaml.dump(out_arr, fo, Dumper=dumper, allow_unicode=True)


if __name__ == '__main__':
    run_export()
