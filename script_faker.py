'''
Use faker to generate test data in database.
'''

import os

import django
from faker import Faker

from config import post_cfg
from torcms.core.tools import get_uu4d, get_uuid

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "administor.settings")
django.setup()
import time
from datetime import datetime

import django.utils.dates
import django.utils.timezone as timezone
from django.test import TestCase

from admin_torcms.models import TabPost, TabPost2Tag, TabTag
from torcms.model.label_model import MPost2Label
from torcms_app.script.command import run_check_jshtml

fak = Faker('zh_CN')
def update_label(post_id, post_data,kind):
    '''
    Update the label when updating.
    '''
    current_tag_infos = MPost2Label.get_by_uid(post_id).objects()
    if 'tags' in post_data:
        pass
    else:
        return False
    if '；' in post_data['tags']:
        tags_arr = [x.strip() for x in post_data['tags'].split('；')]
    elif ',' in post_data['tags']:
        tags_arr = [x.strip() for x in post_data['tags'].split(',')]
    elif '，' in post_data['tags']:
        tags_arr = [x.strip() for x in post_data['tags'].split('，')]
    elif ';' in post_data['tags']:
        tags_arr = [x.strip() for x in post_data['tags'].split(';')]
    else:
        tags_arr = [x.strip() for x in post_data['tags'].split(',')]

    for tag_name in tags_arr:
        if tag_name == '':
            pass
        else:
            MPost2Label.add_record(post_id, tag_name, 1,kind=kind)

    for cur_info in current_tag_infos:
        if cur_info.tag_name in tags_arr:
            pass
        else:
            MPost2Label.remove_relation(post_id, cur_info.tag_id)

def gen_post(tag_uid):
    dt = datetime.now()
    post_uid = f'{key}{get_uu4d()}'
    extinfo = {}
    # 增加地图缺少的信息
    if key == 'm':
        extinfo = {
            'ext_lon':fak.pyfloat(left_digits=3, right_digits=3,min_value=0,max_value=180),
            'ext_lat':fak.pyfloat(left_digits=2, right_digits=3,min_value=0,max_value=90),
            'ext_zoom_current':'4',
            'ext_zoom_max':'7',
            'ext_zoom_min':'1',
        }
    dict_info = {
        'uid': post_uid,
        'title': fak.text(max_nb_chars=5),
        'cnt_md': fak.text(max_nb_chars=300),
        'cnt_html': fak.text(max_nb_chars=300),
        'date': timezone.now(),
        'time_create': dt.timestamp(),
        'time_update': dt.timestamp(),
        'kind': key,
        'extinfo':extinfo
    }
    uu = TabPost.objects.get_or_create(uid=post_uid, defaults=dict_info)
    return post_uid
def gen_label(post_uid,kind):
    post_data = {'tags': '{},{}'.format(fak.text(max_nb_chars=5), fak.text(max_nb_chars=5))}
    update_label(post_uid, post_data,kind)


if __name__ == '__main__':
    # gen()

    for key in post_cfg:
        if key == 's':
            # 需要本地有jshtml文件才能生成app计算工具。
            run_check_jshtml(kind='s')
        else:
            tag_recs = TabTag.objects.filter(kind=key).all()
            for tag_rec in tag_recs:
                for ii in range(10):
                    post_uid = gen_post(tag_rec.uid)
                    print(post_uid)
                    gen_label(post_uid,key)
                    post2tag = TabPost2Tag(
                        uid=get_uuid(),
                        par_id=f'{tag_rec.uid[:2]}00',
                        post_id=post_uid,
                        tag_id=tag_rec.uid,
                        order=0,
                    )
                    post2tag.save()


    #
    # recs = TabPost.objects.filter().all()
    # for rec in recs:
    #     print(rec.title)
    #
    #
