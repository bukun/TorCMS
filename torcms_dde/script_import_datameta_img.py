# -*- coding: utf-8

'''
导入数据集IMG
'''

import os
import sys

sys.path.extend('.')

from pathlib import Path

from PIL import Image

from torcms.model.category_model import TabPost
from torcms.model.post_model import MPost

# logo_cache_dir = './static/cache'
logo_cache_dir = '/home/bk/deploy/fangzai/static/cache'

meta_base = Path('/home/bk/geows/data')


def update_logo(logo, uid):
    entry = TabPost.update(logo=logo).where(TabPost.uid == uid)
    entry.execute()

    return True


def update_db_info(sig):
    pp_data = {'logo': ''}
    # 给数据新的id。

    # 对文件夹内容进行遍历，
    #  对不同文件进行处理。
    for wfile in meta_base.rglob('thumbnail_*'):
        if sig[-4:] in str(wfile.parent):
            hou = wfile.suffix
            if hou in ['.jpg', '.png', '.JPG', '.PNG', 'jpeg', 'JPEG']:
                print('got')
                thum_path = gen_thumb(wfile, sig)
                if thum_path:
                    print(thum_path)
                    pp_data['logo'] = thum_path[len('/home/bk/deploy/fangzai') :]
                    update_logo(pp_data['logo'], sig)


def gen_thumb(img_path, sig):
    img = Image.open(img_path)
    img_width = 400 if img.size[0] > 400 else img.size[0]
    img_height = 300 if img.size[1] > 300 else img.size[1]
    img.thumbnail((img_width, img_height), Image.ANTIALIAS)
    if os.path.exists(logo_cache_dir):
        pass
    else:
        os.mkdir(logo_cache_dir)
    try:
        thum_file_path = os.path.join(logo_cache_dir, 'd' + sig + '.jpg')
        img.save(thum_file_path, "JPEG")
    except Exception:
        thum_file_path = os.path.join(logo_cache_dir, 'd' + sig + '.png')
        img.save(thum_file_path, "PNG")
    return thum_file_path


def import_meta():
    # 此文件夹下声明系统中的数据集及分类
    recs = MPost.query_all(kind='d', limit=10000)
    for rec in recs:
        print('=' * 40)
        uid = rec.uid
        update_db_info(uid)


if __name__ == '__main__':
    import_meta()
