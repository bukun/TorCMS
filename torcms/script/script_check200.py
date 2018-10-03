'''
To Check that the URL could be access via WEB visit.
'''

import requests
import time
from torcms.core.tools import timestamp
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


def run_check200(_):
    '''
    Running the script.
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
                tstr = tstr + DT_STR.format(idx=str(idx).zfill(2), url0=the_url0, code=req.status_code, edit_link=the_url)
                idx = idx + 1

    time_local = time.localtime(timestamp())
    with open('xx200_{d}.html'.format(d=str(time.strftime("%Y_%m_%d", time_local))), 'w') as fileo:
        fileo.write(HTML_TMPL.format(cnt=tstr))
    print('Checking 200 finished.')
