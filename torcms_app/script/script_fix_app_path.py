# -*- coding: UTF-8 -*-


import os
import sys

import tornado.escape
from bs4 import BeautifulSoup

from torcms.core import tools

pwd = os.getcwd()
(qian, hou) = os.path.split(pwd)
sys.path.append(qian)

from torcms_app.model.ext_model import MAppYun
from config import APP_MASK

mequ = MAppYun()

xx = range(0, 16)
yy = [hex(x) for x in xx]
yy = [y[-1] for y in yy]


def javascript2database(htmlfile, html_path, kind='s'):
    # print(kind)
    (wroot, wfile) = os.path.split(htmlfile)
    (qian, hou) = os.path.splitext(wfile)
    sig4 = qian.split('_')[0]
    html_cnt = open(htmlfile).read()
    soup = BeautifulSoup(html_cnt, 'html.parser')
    desc = ''
    # print (soup('title'))
    for meta_tag in soup('meta'):

        # if 'name' in meta_tag:
        try:
            if meta_tag['name'] == 'description':
                desc = meta_tag['content']
        except:
            pass

    sig = 's' + sig4

    js_dic = {
        'sig': sig,
        'title': 'No Title' if (soup.title is None) else str(soup.title.string).strip(),
        'desc': desc.strip(),
        'html_path': tornado.escape.xhtml_escape(os.path.splitext(html_path)[0]),
        'cnt_md': 'MarkDown Content.',
        'cnt_html': 'HTML Content.',
        'time_create': tools.timestamp(),
        'kind': kind,  # Todo:
    }
    mequ.addata_init(js_dic)


def test_valid(wfile):
    '''
    Test the file in App HTML File.
    :param wfile:
    :return:
    '''
    if wfile.endswith('.html'):
        pass
    else:
        return False
    if wfile.endswith('_js.html'):
        return False
    (qian, hou) = os.path.splitext(wfile)
    sig = qian.split('_')[0]

    for x in sig:
        if x in yy:
            pass
        else:
            return False

    return True


def run_fix_path(kind='s'):
    javascript_ws = './templates/jshtml'
    for wroot, wdirs, wfiles in os.walk(javascript_ws):
        for wfile in wfiles:
            if test_valid(wfile):
                infile = os.path.join(wroot, wfile)
                # print(infile)
            else:
                continue
            html_path = infile[len(javascript_ws) + 1:]

            for appmask in APP_MASK:
                if appmask in infile:
                    print('Go ..')
                    continue
                else:
                    javascript2database(infile, html_path, kind=kind)
