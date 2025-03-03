# -*- coding:utf-8 -*-
'''
Export posts from database to Markdown files.
'''

import os
import re
import shutil
from pathlib import Path

import markdown

from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost

out_ws = Path(__file__).parent / 'xx_mds'


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
    pid = rec.pid
    cat_id = rec.uid
    out_base_dir = os.path.join(
        out_ws, pid, 'ch{}_{}_{}'.format(rec.order, rec.uid, '_'.join(rec.name.split()))
    )
    if os.path.exists(out_base_dir):
        pass
    else:
        os.makedirs(out_base_dir)

    post2tag_recs = MPost2Catalog.query_by_catid(cat_id)
    for post2tag_rec in post2tag_recs:
        print(post2tag_rec.post_id)
        postinfo = MPost.get_by_uid(post2tag_rec.post_id)
        markdown_cnt = postinfo.cnt_md
        md = markdown.Markdown(extensions=['meta'])
        html = "{ " + md.convert(markdown_cnt) + " }"

        print("*" * 50)
        print(md.Meta)
        stitle = md.Meta.get('s-title')
        if stitle:
            stitle = stitle[0].strip()
        else:
            stitle = postinfo.title.strip().replace('/', '-').replace(' ', '_')

        out_cat_dir = os.path.join(
            out_base_dir,
            'sec{}_'.format(post2tag_rec.order)
            + '_'.join(stitle.split())
            + '_uid'
            + post2tag_rec.post_id,
        )

        if os.path.exists(out_cat_dir):
            pass
        else:
            os.makedirs(out_cat_dir)

        logo = postinfo.logo
        logo_name = os.path.split(logo)[-1]
        if logo.startswith('http'):
            # 下面代码，可同时处理 http 与 https
            img_path = './' + logo[len('http://www.osgeo.cn/') :].strip('/')

            out_img_path = os.path.join(out_cat_dir, logo_name)
            if os.path.exists(img_path):
                shutil.copy(img_path, out_img_path)
            logo = out_img_path

        elif logo.startswith('//www.osgeo.cn'):
            img_path = './' + logo[len('//www.osgeo.cn/') :].strip('/')
            print(img_path)
            out_img_path = os.path.join(out_cat_dir, logo_name)
            if os.path.exists(img_path):
                shutil.copy(img_path, out_img_path)
            logo = out_img_path

        elif logo.startswith('/static'):
            img_path = '.' + logo
            out_img_path = os.path.join(out_cat_dir, logo_name)
            if os.path.exists(img_path):
                shutil.copy(img_path, out_img_path)
            logo = out_img_path
        else:
            pass

        # 拷贝图片到同一文件夹
        imgs = get_img(postinfo.cnt_md)
        for img in imgs:
            img_url = img.strip(')').split('(')[-1]
            img_name = os.path.split(img_url)[-1]
            if img_url.startswith('http'):
                # 下面代码，可同时处理 http 与 https
                img_path = './' + img_url[len('http://www.osgeo.cn/') :].strip('/')
                print(img_path)
                out_img_path = os.path.join(out_cat_dir, img_name)
                if os.path.exists(img_path):
                    shutil.copy(img_path, out_img_path)

                markdown_cnt = markdown_cnt.replace(img_url, img_name)

            elif img_url.startswith('//www.osgeo.cn'):
                img_path = './' + img_url[len('//www.osgeo.cn/') :].strip('/')
                print(img_path)
                out_img_path = os.path.join(out_cat_dir, img_name)
                if os.path.exists(img_path):
                    shutil.copy(img_path, out_img_path)

                markdown_cnt = markdown_cnt.replace(img_url, img_name)

            elif img_url.startswith('/static'):
                img_path = '.' + img_url
                out_img_path = os.path.join(out_cat_dir, img_name)
                if os.path.exists(img_path):
                    shutil.copy(img_path, out_img_path)
                markdown_cnt = markdown_cnt.replace(img_url, img_name)
            else:
                pass

        out_file = os.path.join(out_cat_dir, stitle + '.md')

        with open(out_file, 'w') as fout_md:
            if md.Meta.get('title'):
                pass
            else:
                fout_md.write('title: {}\n'.format(postinfo.title))

            if md.Meta.get('s-title'):
                pass
            else:
                fout_md.write('s-title: {}\n'.format(stitle))
            if md.Meta.get('logo'):
                pass
            else:
                fout_md.write('logo: {}\n'.format(logo))
            if md.Meta.get('order'):
                pass
            else:
                fout_md.write('order: {}\n'.format(postinfo.order))

            if md.Meta.get('date'):
                pass
            else:
                fout_md.write('date: {}\n'.format(postinfo.time_update))

            if md.Meta.get('author'):
                pass
            else:
                fout_md.write('author: {}\n'.format(postinfo.user_name))

            if md.Meta.get('cnt_md'):
                pass
            else:
                fout_md.write(
                    'cnt_md: {}\n'.format(
                        "{ " + markdown_cnt.replace('\r\n', '\n') + " }"
                    )
                )
            if md.Meta.get('cnt_html'):
                pass
            else:
                fout_md.write('cnt_html: {}\n'.format(html))
            if md.Meta.get('memo'):
                pass
            else:
                fout_md.write('memo: {}\n'.format(postinfo.memo))

            if md.Meta.get('extinfo'):
                pass
            else:
                fout_md.write('extinfo: {}\n\n'.format(postinfo.extinfo))


def test_run_export():
    all_cats = MCategory.query_all('1')
    for rec in all_cats:
        if rec.pid == '0000':
            continue

        else:
            do_for_cat(rec)

    # if os.path.exists(out_ws):
    #     shutil.rmtree(out_ws)


if __name__ == '__main__':
    test_run_export()
