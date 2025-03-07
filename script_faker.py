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

fak = Faker('zh_CN')


# def gen():
#     for key in post_cfg:
#         print(key)
#         dt = datetime.now()
#
#         post = TabPost(
#             uid=f'{key}{get_uu4d()}',
#             title=fak.text(max_nb_chars=16),
#             cnt_md=fak.text(max_nb_chars=300),
#             cnt_html=fak.text(max_nb_chars=300),
#             date=timezone.now(),
#             time_create=dt.timestamp(),
#             time_update=dt.timestamp(),
#         )
#
#         post.save()


if __name__ == '__main__':
    # gen()

    for key in post_cfg:
        tag_recs = TabTag.objects.filter(kind=key ).all()

        for tag_rec in tag_recs:
            for ii  in range(10):
                dt = datetime.now()
                post_uid = f'{key}{get_uu4d()}'
                dict_info =       {
                    'uid':  post_uid,
                'title':  fak.text(max_nb_chars=16),
                'cnt_md':  fak.text(max_nb_chars=300),
                'cnt_html':  fak.text(max_nb_chars=300),
                'date':  timezone.now(),
                'time_create':  dt.timestamp(),
                'time_update':  dt.timestamp(),
                    'kind':  key,
                }
                uu = TabPost.objects.get_or_create(uid=post_uid, defaults=dict_info)
                print(post_uid)
                # print(uu.uid)
                # post = TabPost(
                #
                # )
                #
                # post.save()

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


