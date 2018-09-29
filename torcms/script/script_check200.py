'''
To Check that the URL could be access via WEB visit.
'''

from torcms.model.post_model import MPost
# from torcms.model.wiki_model import MWiki
import requests
import time
from torcms.core.tools import timestamp
import config

HTML_TMPL = '''
<!doctype html><html><head><title></title></head><body>
<dl>{cnt}</dl></body></html>
'''

DT_STR = '''<dt>{title}</dt><dd>{uid}</dd>
<dd><a href="{edit_link}">{edit_link}</a></dd>'''


def run_check200(_):
    '''
    Running the script.
    '''

    tstr = ''

    for kind in config.router_post.keys():
        posts = MPost.query_all(kind=kind, limit=20000)
        for index, post in enumerate(posts):
            the_url0 = '{site_url}/{kind_url}/{uid}'.format(
                site_url=config.SITE_CFG['site_url'],
                kind_url=config.router_post[post.kind],
                uid=post.uid)

            the_url = '{site_url}/{kind_url}/_edit/{uid}'.format(
                site_url=config.SITE_CFG['site_url'],
                kind_url=config.router_post[post.kind],
                uid=post.uid)
            uu = requests.get(the_url0)

            if uu.status_code == 200:
                pass
            else:
                tstr = tstr + DT_STR.format(title=the_url0, uid=uu.status_code, edit_link=the_url)

    timeit = timestamp()
    time_local = time.localtime(timeit)
    with open('xx_posts_x200_{date0}.html'.format(
            date0=str(time.strftime("%Y_%m_%d", time_local))),
            'w') as fo:
        fo.write(HTML_TMPL.format(cnt=tstr))
    print('Checking 200 finished.')
