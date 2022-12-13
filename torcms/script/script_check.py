# -*- coding: utf-8 -*-

'''
检查的脚本
'''

import time

import requests

# from torcms.model.wiki_model import MWiki
import config
from config import router_post
from torcms.core.tools import timestamp
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost

HTML_TMPL = '''<!doctype html><html><head><title></title>
<script src="https://www.osgeo.cn/_f2elib/jquery/jquery-3.6.min.js"></script>
<script src="https://www.osgeo.cn/_f2elib/bootstrap-3.4/js/bootstrap.min.js"></script>
<script src="https://www.osgeo.cn/_f2elib/jquery-validate_1.15.0/jquery.validate.min.js"></script>
<script src="https://www.osgeo.cn/_f2elib/magnific-popup_1.1.0/jquery.magnific-popup.min.js"></script>
<script src="https://www.osgeo.cn/_f2elib/leaflet-1.9/leaflet.js"></script>
<script src="https://www.osgeo.cn/_f2elib/leaflet/leaflet.ChineseTmsProviders.js"></script>
<link rel="stylesheet" href="https://www.osgeo.cn/_f2elib/bootstrap_3.3.7/css/bootstrap.min.css">
<link rel="stylesheet" href="https://www.osgeo.cn/_f2elib/leaflet-1.9/leaflet.css">
</head>
<body>
<div class="container">
    <div class="row" >
        <div class="col-xs-12 col-sm-12">
            <div class="panel panel-default">
                <div class="panel-heading">
                Error .
                </div>
                <div class="panel-body">
                    <dl class="table">{cnt}</dl>
                </div>
            </div>
        </div>
    </div>
</div>

</body></html>
'''

DT_STR = '''<dt>{idx} : {url0} </dt>
<dd>{code}</dd>
<dd>
<a href="{edit_link}" target="_blank">
{edit_link}
</a>
</dd>
<dd>
<a href="{edit_tag_link}" target="_blank">
{edit_tag_link}
</a>
</dd>
<hr />
'''


def check200():
    '''
    对可以通过 WEB 访问的 URL 进行检查
    '''
    print('Checking HTTP 200 error: ')

    tstr = ''
    idx = 1
    for kind in config.router_post.keys():
        posts = MPost.query_all(kind=kind, limit=20000)
        for post in posts:
            the_url0 = '{site_url}/{kind_url}/{uid}'.format(
                site_url=config.SITE_CFG['site_url'],
                kind_url=config.router_post[post.kind],
                uid=post.uid)

            the_url = '{site_url}/{kind_url}/_edit/{uid}'.format(
                site_url=config.SITE_CFG['site_url'],
                kind_url=config.router_post[post.kind],
                uid=post.uid)

            the_url2 = '{site_url}/{kind_url}/_edit_kind/{uid}'.format(
                site_url=config.SITE_CFG['site_url'],
                kind_url=config.router_post[post.kind],
                uid=post.uid)

            req = requests.get(the_url0)

            if req.status_code == 200:
                pass
            else:
                print(the_url0)
                tstr = tstr + DT_STR.format(
                    idx=str(idx).zfill(2),
                    url0=the_url0,
                    code=req.status_code,
                    edit_link=the_url,
                    edit_tag_link=the_url2,
                )
                idx = idx + 1

    time_local = time.localtime(timestamp())
    with open(
            'xx_err_200_{d}.html'.format(
                d=str(time.strftime("%Y_%m_%d", time_local))), 'w') as fileo:
        fileo.write(HTML_TMPL.format(cnt=tstr))
    print('Checking 200 finished.')


def check_kind():
    '''
    对 post 与 对应类型的 kind 进行检查
    '''
    for kindv in router_post:
        for rec_cat in MCategory.query_all(kind=kindv):
            catid = rec_cat.uid
            catinfo = MCategory.get_by_uid(catid)
            for rec_post2tag in MPost2Catalog.query_by_catid(catid):
                postinfo = MPost.get_by_uid(rec_post2tag.post_id)
                if postinfo.kind == catinfo.kind:
                    pass
                else:
                    print(postinfo.uid)


def check_tag():
    '''
    Checking the post of error tags.
    '''
    print('Checking tag error: ')
    tstr = ''
    idx = 1
    for kind in config.router_post.keys():
        posts = MPost.query_all(kind=kind, limit=20000)

        for post in posts:

            p_catinfo = None

            post2catinfo = MPost2Catalog.get_first_category(post.uid)
            if post2catinfo:
                catinfo = MCategory.get_by_uid(post2catinfo.tag_id)
                if catinfo:
                    p_catinfo = MCategory.get_by_uid(catinfo.pid)

            if post.extinfo.get('def_cat_pid') and post.extinfo.get(
                    'gcat0') and p_catinfo:

                pass
            else:
                the_url0 = '{site_url}/{kind_url}/{uid}'.format(
                    site_url=config.SITE_CFG['site_url'],
                    kind_url=config.router_post[post.kind],
                    uid=post.uid)

                the_url = '{site_url}/{kind_url}/_edit/{uid}'.format(
                    site_url=config.SITE_CFG['site_url'],
                    kind_url=config.router_post[post.kind],
                    uid=post.uid)
                the_url2 = '{site_url}/{kind_url}/_edit_kind/{uid}'.format(
                    site_url=config.SITE_CFG['site_url'],
                    kind_url=config.router_post[post.kind],
                    uid=post.uid)
                req = requests.get(the_url0)

                if req.status_code == 200:
                    pass
                else:
                    print(the_url0)
                    tstr = tstr + DT_STR.format(
                        idx=str(idx).zfill(2),
                        url0=the_url0,
                        code=req.status_code,
                        edit_link=the_url,
                        edit_tag_link=the_url2,
                    )
                    idx = idx + 1

    time_local = time.localtime(timestamp())
    with open(
            'xx_err_tag_{d}.html'.format(
                d=str(time.strftime("%Y_%m_%d", time_local))), 'w') as fileo:
        fileo.write(HTML_TMPL.format(cnt=tstr))
    print('Checking 200 finished.')


def run_check(_):
    check_tag()
    check_kind()
    check200()
