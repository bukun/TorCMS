# -*- coding: utf-8 -*-

'''
Generating sitemap.
'''
import os
from torcms.model.post_model import MPost
from torcms.model.wiki_model import MWiki
from config import router_post, SITE_CFG

SITE_MAP_FILE = 'xx_sitemap.txt'


def gen_post_map():
    mpost = MPost()
    with open(SITE_MAP_FILE, 'a') as fo:
        for kind_key in router_post:
            recent_posts = mpost.query_all(kind=kind_key, limit=1000000)
            for recent_post in recent_posts:
                url = os.path.join(SITE_CFG['site_url'],
                                   router_post[recent_post.kind],
                                   recent_post.uid)
                fo.write('{url}\n'.format(url=url))


def gen_wiki_map():
    mwiki = MWiki()

    # wiki
    wiki_recs = mwiki.query_all(limit=10000, kind='1')

    with open(SITE_MAP_FILE, 'a') as fileout:
        for rec in wiki_recs:
            url = os.path.join(SITE_CFG['site_url'], 'wiki', rec.title)
            fileout.write('{url}\n'.format(url=url))

    ## page.
    page_recs = mwiki.query_all(limit=10000, kind='2')

    with open(SITE_MAP_FILE, 'a') as fileout:
        for rec in page_recs:
            url = os.path.join(SITE_CFG['site_url'], 'page', rec.uid)

            fileout.write('{url}\n'.format(url=url))


def run_sitemap(*args):
    if os.path.exists(SITE_MAP_FILE):
        os.remove(SITE_MAP_FILE)

    gen_wiki_map()
    gen_post_map()
