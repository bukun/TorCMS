# -*- coding: utf-8 -*-

import os

from torcms.model.post_model import MPost
from torcms.model.wiki_model import MWiki

from config import router_post
from config import site_url

SiteMapFile = 'sitemap.txt'


def gen_post_map():
    mpost = MPost()
    with open(SiteMapFile, 'a') as fo:
        for key in router_post.keys():
            recent_posts = mpost.query_all(kind=key)
            for recent_post in recent_posts:
                url = os.path.join(site_url, router_post[recent_post.kind], recent_post.uid)
                fo.write('{url}\n'.format(url=url))


def gen_wiki_map():
    mwiki = MWiki()

    # wiki
    wiki_recs = mwiki.query_all(limit=10000, kind='1')

    with open(SiteMapFile, 'a') as fo:
        for rec in wiki_recs:
            url = os.path.join(site_url, 'wiki', rec.title)
            fo.write('{url}\n'.format(url=url))

    ## page.
    page_recs = mwiki.query_all(limit=10000, kind='2')

    with open(SiteMapFile, 'a') as fo:
        for rec in page_recs:
            url = os.path.join(site_url, 'page', rec.uid)

            fo.write('{url}\n'.format(url=url))


def run_sitemap():
    if os.path.exists(SiteMapFile):
        os.remove(SiteMapFile)

    gen_wiki_map()
    gen_post_map()
