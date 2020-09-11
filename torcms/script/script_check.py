'''
检查的脚本
'''

import requests
import time

from config import router_post
from torcms.core.tools import timestamp
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
# from torcms.model.wiki_model import MWiki
import config

HTML_TMPL = '''<!doctype html><html><head><title></title></head>
<body>
<dl class="table">{cnt}</dl>
</body></html>
'''

DT_STR = '''<dt>{idx} : {url0} </dt>
<dd>{code}</dd>
<dd>
<a href="{edit_link}" target="_blank">
{edit_link}
</a>
</dd>
<hr />
'''


def run_check200():
    '''
    对可以通过 WEB 访问的 URL 进行检查
    '''

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
            req = requests.get(the_url0)

            if req.status_code == 200:
                pass
            else:
                print(the_url0)
                tstr = tstr + DT_STR.format(idx=str(idx).zfill(2), url0=the_url0, code=req.status_code,
                                            edit_link=the_url)
                idx = idx + 1

    time_local = time.localtime(timestamp())
    with open('xx200_{d}.html'.format(d=str(time.strftime("%Y_%m_%d", time_local))), 'w') as fileo:
        fileo.write(HTML_TMPL.format(cnt=tstr))
    print('Checking 200 finished.')


def run_check_kind():
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


def run_check(_):
    run_check200()
    run_check_kind()
