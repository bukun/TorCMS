# -*- coding:utf8-*-

'''
导入 Jupyter 格式的文档
'''

import os
import sys
from pathlib import Path
from torcms.model.category_model import MCategory
from torcms.model.post_model import MPost
from torcms.handlers.post_handler import update_category
from torcms.model.core_tab import TabTag
import bs4
import re
import subprocess
from torcms.core.tools import get_uu4d, get_uu8d
import shutil

pwd = os.getcwd()


def get_docker_name(the_str):
    # the_str = 'sd_dc-asdf/fdsaf_dc-wdsfadf/asdf'
    regobj = re.compile('_dc-\w*/')

    tt = regobj.search(the_str).span()

    print(tt)
    return the_str[tt[0]: tt[1]][4: -1]

def split_text(inws, in_text):
    '''
    根据正则表达式，找到特殊的字符串。
    对原始字符串进行切分。
    返回切分的结果，以及用来切分的特殊字符串。def get_docker_name(the_str):
    regobj = re.compile('\d\d\d-\d\d\d-\d\d\d\d')
    tt = regobj.search(the_str)
    print(tt)

    '''

    # in_text = in_text.replace('{', '{{').replace('}', '}}')

    # ToDo: '*,', '*.' ， 未处理。

    # 术语、参考
    phoneNumRegex = re.compile('|'.join(rest_regs))
    # print(in_text)
    in_text = str(in_text)

    out_reg_arr = phoneNumRegex.findall(in_text)
    #     print(out_reg_arr)
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
                # print('=' * 40)
                bb = bb.strip('"')
                iiis = bb.split('/')
                img = iiis[-1]
                # print(img)

                # ToDo: 图像的查找路径需要修改
                img_path = Path(inws)
                for wfile in img_path.rglob('*'):
                    # print('-' * 20)
                    # print(wfile.name)
                    if img == wfile.name:
                        img = str(wfile.resolve())[len(pwd):]
                # print(img)
                tt.append('src="{}"'.format(img))
            else:
                tt.append(bb)

        outarr.append('<img {} />'.format(' '.join(tt)))
    return outarr
    # return '<img {} />'.format(' '.join(tt))


rest_regs = [
    # '\s:.+?:`.+?`\/:.+?:`.+?`\/:.+?:`.+?`'
    '\<img.+?\/\>',  # 形如：   ``sadf``: :sdf:`slfkj`

]


def do_for_chapter(cat_id, ch_path):
    '''
    对章的“节”内容进行处理
    '''
    idx = 1
    for jufile in Path(ch_path).rglob('sec*.ipynb'):
        print(jufile.name)
        the_pp = str(jufile.absolute().resolve())
        print(the_pp)
        docker_name = get_docker_name(the_pp)

        print(docker_name)
        print('=' * 40)
        print(jufile)

        uid = jufile.stem.split('_')[-1]
        print(uid)
        subprocess.run(f'jupyter nbconvert --to html {jufile.resolve()} --output /tmp/xx.html ', shell=True)

        pp_data = get_meta(cat_id, idx, uid, docker_name)
        print('u' * 40)
        xx_data = pp_data.copy()
        xx_data.pop('cnt_md')
        # xx_data.pop('cnt_html')
        print(xx_data)

        # pprint(pp_data)
        # 入库是将外扩展字段加入。
        MPost.add_or_update_post(pp_data['uid'], pp_data, extinfo=pp_data['extinfo'])
        update_category(pp_data['uid'], pp_data)
        idx = idx + 1

def get_appfile(uid):
    ws_raw = Path('./static/judocs')
    ws_aim = Path('./static/xnb')

    if ws_aim.exists():
        pass
    else:
        ws_aim.mkdir()


    wfiles = ws_raw.rglob(f'*{uid}.ipynb')

    aimfiles = list(ws_aim.rglob(f'*{uid}.ipynb'))

    wfiles = list(wfiles)

    match_count = len(wfiles)

    if match_count == 1:
        if len(aimfiles) == 1:
            print('--=-=-=-==-=-=')
            print(str(aimfiles[0]))
            # 缩短了文件路径，只保留了static以后的路径
            return str(aimfiles[0])
        else:
            app_7z = wfiles[0]
            salt = get_uu8d()
            new_file = f'jupy{salt}_{uid}{app_7z.suffix}'.lower()
            print('copy ... ')
            new_file_path = ws_aim / new_file
            shutil.copy(
                app_7z,
                new_file_path
            )
            return str(Path(new_file_path).resolve())
    else:
        print(uid)
    return ''

def get_meta(catid, idx, uid, docker_name):
    '''
    Get metadata of dataset via ID.
    '''
    html_file = '/tmp/xx.html'
    # File = open(str(the_file.resolve()))
    Soup = bs4.BeautifulSoup(open(html_file).read(), features="html.parser")
    title = Soup.select('h1')[0].getText()
    content = Soup.select('#notebook-container')[0]
    print('========1111')

    # title.replace('{', '{{').replace('}', '}}')
    uu, vv = split_text(inws, content)
    # content = vv.join(uu)

    # print(len(uu))
    # print(len(vv))
    result = [None] * (len(uu) + len(vv))
    result[::2] = uu
    result[1::2] = vv
    content = ' '.join(result)

    # print('\033[0m')
    # content  = content.replace('&#182;', '')

    pp_data = {}
    pp_data['uid'] = uid
    pp_data['title'] = str(title)[:-1]
    pp_data['cnt_md'] = str(content).replace('class="container"','')
    pp_data['user_name'] = 'admin'
    pp_data['def_cat_uid'] = catid
    pp_data['gcat0'] = catid
    pp_data['def_cat_pid'] = catid[:2] + '00'
    pp_data['logo'] = ''
    pp_data['kind'] = 'k'
    pp_data['valid'] = 1
    pp_data['order'] = idx
    # 将主要数据添加到外扩展
    pp_data['extinfo'] = {
        'wx_vecode': get_uu4d(),
        'wx_dolink': get_appfile(uid),
        'dc_image': docker_name,
        'dc_uid': uid,
    }
    # 将kind修改为'k',输出外扩展方便查看验证码。
    print(pp_data['extinfo'])
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


def bainli(inws):
    all_recs = TabTag.select()
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
            cat_path = Path(os.path.join(wroot, wdir))
            print(cat_path.name)

            # 过滤 doctrees/ 目录, 获取html目录中的内容


            # 根据内容中的H1获取分类名称
            get_cat_name = get_catname(cat_path, 'chapter')

            if get_cat_name:
                cat_name = str(get_cat_name)[:-1]
            else:
                cat_name = cat_slug

            post_data = {'name': cat_name,
                         'slug': cat_slug.lower(),
                         'order': idx,
                         'kind': 'k',
                         'pid': pid}

            try:
                MCategory.add_or_update(cat_id, post_data)
            except Exception:
                pass

            do_for_chapter(
                cat_id,
                Path(os.path.join(wroot, wdir))
            )


            idx = idx + 1


if __name__ == '__main__':

    inws = 'static/judocs'
    bainli(inws)
