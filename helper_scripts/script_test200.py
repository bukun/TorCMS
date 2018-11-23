from torcms.model.post_model import MPost
from torcms.model.wiki_model import MWiki
import requests
import config
from torcms.core.tools import timestamp
from torcms.core.tools import format_date
import time

html_tmpl = '''
<!doctype html>
<html>
<head>
<title></title>
</head>
<body>
<dl>
{cnt}
</dl>
</body>
</html>
'''

dt_str = '''
<dt>{title}</dt>
<dd>{uid}</dd>
<dd><a href="{edit_link}">{edit_link}</a></dd>
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
            # print(index)
            # print(post.uid)
            pass
        else:
            print(index)
            print(the_url)
            print(uu.status_code)
            tstr = tstr + dt_str.format(title=the_url0, uid=uu.status_code, edit_link=the_url)

timeit = timestamp()
time_local = time.localtime(timeit)
with open('xx_posts_x200_{date0}.html'.format(
        date0=str(time.strftime("%Y_%m_%d", time_local))),
        'w') as fo:
    fo.write(html_tmpl.format(cnt=tstr))
