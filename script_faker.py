'''
Use faker to generate test data in database.
'''

import os
import pathlib
import re
import sys

import bs4
import django
from faker import Faker

from config import post_cfg
from torcms.core.tools import get_uu4d, get_uuid
from torcms.handlers.post_handler import update_category
from torcms.model.category_model import MCategory
from torcms.model.post_model import MPost
from torcms.model.wiki_model import MWiki

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "administor.settings")
django.setup()
from datetime import datetime

import django.utils.timezone as timezone

from admin_torcms.models import TabPost, TabPost2Tag, TabTag
from torcms.model.label_model import MPost2Label
from torcms_app.script.command import run_check_jshtml

fak = Faker('zh_CN')

rest_regs = [
    '\<img.+?\/\>',
]


def update_label(post_id, post_data):
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
            MPost2Label.add_record(post_id, tag_name, 1)

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
            'ext_lon': fak.pyfloat(
                left_digits=3, right_digits=3, min_value=0, max_value=180
            ),
            'ext_lat': fak.pyfloat(
                left_digits=2, right_digits=3, min_value=0, max_value=90
            ),
            'ext_zoom_current': '4',
            'ext_zoom_max': '7',
            'ext_zoom_min': '1',
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
        'extinfo': extinfo,
    }
    uu = TabPost.objects.get_or_create(uid=post_uid, defaults=dict_info)
    return post_uid


def gen_label(post_uid, kind):
    post_data = {
        'tags': '{},{}'.format(fak.text(max_nb_chars=5), fak.text(max_nb_chars=5))
    }
    update_label(post_uid, post_data)


pwd = os.getcwd()


def split_text(inws, in_text):
    phoneNumRegex = re.compile('|'.join(rest_regs))
    in_text = str(in_text)

    out_reg_arr = phoneNumRegex.findall(in_text)
    out_reg_arr = filter_reg_text(inws, out_reg_arr)

    if out_reg_arr:
        out_text_arr = phoneNumRegex.split(in_text)
    else:
        out_text_arr = [in_text]

    return out_text_arr, out_reg_arr


def filter_reg_text(inws, out_reg_arr):
    outarr = []

    for item in out_reg_arr:
        item = item[5:-2]
        bbs = item.split()

        tt = []
        for bb in bbs:
            if bb.startswith('src'):
                bb = bb.strip('"')
                iiis = bb.split('/')
                img = iiis[-1]

                img_path = pathlib.Path(inws)
                for wfile in img_path.rglob('*'):
                    if img == wfile.name:
                        img = str(wfile.resolve())[len(pwd) :]
                tt.append('src="{}"'.format(img))
            else:
                tt.append(bb)

        outarr.append('<img {} />'.format(' '.join(tt)))
    return outarr


def do_for_chapter(cat_id, ch_path):
    file_path = []
    idx = 1
    for conpath in ch_path.iterdir():
        if conpath.name.lower().startswith('sec'):
            file_path.append(conpath)
        else:
            continue

    file_path.sort()

    for x in file_path:
        for s in x.rglob('*.html'):
            if s.name.startswith('section'):
                pass
            else:
                continue
            if idx == 10:
                uu = 'a'
            else:
                uu = idx
            sig = cat_id + str(uu)
            pp_data = get_meta(cat_id, sig, s, idx)
            MPost.add_or_update_post(pp_data['uid'], pp_data, extinfo={})
            update_category(pp_data['uid'], pp_data)
            idx = idx + 1


def do_for_page(cat_id, ch_path, filename, idx):
    for x in ch_path.rglob('*.html'):
        if x.name.startswith(filename):
            pass
        else:
            continue

        pp_data = get_page_meta(cat_id, x, idx)
        if MWiki.get_by_uid(cat_id):
            MWiki.update(cat_id, pp_data)
        else:
            MWiki.create_page(cat_id, pp_data)


def get_page_meta(catid, the_file, idx):
    print(the_file.name)
    File = open(str(the_file.resolve()))
    Soup = bs4.BeautifulSoup(File.read(), features="html.parser")
    title = Soup.select('title')
    content = Soup.select('.body')[0]
    conz = ''
    for a in content.find_all(["h1", "p"]):
        conz += str(a)

    pp_data = {}
    pp_data['uid'] = catid
    pp_data['title'] = title[0].getText() + str(idx)
    pp_data['cnt_md'] = conz
    pp_data['user_name'] = 'admin'

    return pp_data


def get_meta(catid, sig, the_file, idx):
    File = open(str(the_file.resolve()))
    Soup = bs4.BeautifulSoup(File.read(), features="html.parser")
    title = Soup.select('h1')[0].getText()
    content = Soup.select('.body')[0]
    uu, vv = split_text(inws, content)
    result = [None] * (len(uu) + len(vv))
    result[::2] = uu
    result[1::2] = vv
    content = ' '.join(result)

    pp_data = {}
    pp_data['uid'] = sig
    pp_data['title'] = str(title)[:-1]
    pp_data['cnt_md'] = str(content)
    pp_data['user_name'] = 'admin'
    pp_data['def_cat_uid'] = catid
    pp_data['gcat0'] = catid
    pp_data['def_cat_pid'] = catid[:2] + '00'
    pp_data['logo'] = ''
    pp_data['kind'] = 'k'
    pp_data['valid'] = 1
    pp_data['order'] = idx
    # 将主要数据添加到外扩展
    pp_data['extinfo'] = {}

    return pp_data


def get_catname(ch_path, filename):
    for x in ch_path.rglob('*.html'):
        if x.name.startswith(filename):
            pass
        else:
            continue
        print(x.name)

        File = open(str(x.resolve()))
        Soup = bs4.BeautifulSoup(File.read(), features="html.parser")
        content = Soup.select('.body')[0]
        title = content.find_all("h1")[0].get_text()
        return title


def bianli(inws):
    all_recs = TabTag.objects.filter().all()
    recs_arr = []
    for x in all_recs:
        recs_arr.append(x.order)

    # 对新插入的文章，重新进行编号。 因为只是相对序号，所以取了最大值后，再依序后排。
    max_order = max(recs_arr)
    print("-" * 50)
    print(max(recs_arr))

    for wroot, wdirs, wfiles in os.walk(inws):
        if 'doctrees' in wroot:
            continue
        idx = max_order + 1

        for wdir in wdirs:
            if wdir.startswith('ch') and len(wdir.split('_')) > 2:
                pass
            else:
                continue

            cat_id = wdir.split('_')[1]
            cat_slug = wdir.split('_')[2]
            pid = cat_id[:2] + '00'
            cat_path = pathlib.Path(os.path.join(wroot, wdir))
            print(cat_path.name)

            # 过滤 doctrees/ 目录, 获取html目录中的内容
            is_html = str(cat_path).split('/')[3]
            if is_html == 'html':
                pass
            else:
                continue

            # 根据内容中的H1获取分类名称
            get_cat_name = get_catname(cat_path, 'chapter')

            if get_cat_name:
                cat_name = str(get_cat_name)[:-1]
            else:
                cat_name = cat_slug

            post_data = {
                'name': cat_name,
                'slug': cat_slug.lower(),
                'order': idx,
                'kind': 'k',
                'pid': pid,
            }

            try:
                MCategory.add_or_update(cat_id, post_data)
            except Exception:
                pass

            do_for_chapter(cat_id, pathlib.Path(os.path.join(wroot, wdir)))

            #  将 chapter.html 内容存入数据库， page/catid 形式访问
            do_for_page(cat_id, pathlib.Path(os.path.join(wroot, wdir)), 'chapter', idx)
            #  将 index.html 内容存入数据库， page/catid 形式访问
            do_for_page(pid, pathlib.Path(os.path.join(wroot)), 'index', idx)

            idx = idx + 1


if __name__ == '__main__':
    # gen()

    for key in post_cfg:
        if key == 's':
            # 需要本地有jshtml文件才能生成app计算工具。
            run_check_jshtml(kind='s')
        elif key == 'k':
            # 教程导入，需要有教程文件。
            if len(sys.argv) < 2:
                uu = '_build_GIS_A'
            else:
                uu = sys.argv[1]

            inws = os.path.join('static/xx_tuto_html', uu)

            bianli(inws)

        else:
            tag_recs = TabTag.objects.filter(kind=key).all()
            for tag_rec in tag_recs:
                if tag_rec.uid.endswith('00'):
                    continue
                for ii in range(10):
                    post_uid = gen_post(tag_rec.uid)
                    print(post_uid)
                    gen_label(post_uid, key)
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
