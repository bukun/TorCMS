# -*- coding: utf-8 -*-
'''
Generating sitemap.
'''
import os

from config import SITE_CFG, router_post
from torcms.model.post_model import MPost
from torcms.model.wiki_model import MWiki


def gen_post_map(file_name, ext_url=''):
    '''
    Generate the urls for posts.
    :return: None
    '''
    with open(file_name, 'a') as fout:
        for kind_key in router_post:
            recent_posts = MPost.query_all(kind=kind_key, limit=1000000)
            for recent_post in recent_posts:
                url = os.path.join(SITE_CFG['site_url'],
                                   router_post[recent_post.kind], ext_url,
                                   recent_post.uid)
                fout.write('{url}\n'.format(url=url))


def gen_wiki_map(file_name, ext_url=''):
    '''
    Generate the urls for wiki.
    :return: None
    '''

    # for wiki.
    wiki_recs = MWiki.query_all(limit=10000, kind='1')

    with open(file_name, 'a') as fileout:
        for rec in wiki_recs:
            url = os.path.join(SITE_CFG['site_url'],
                               'wiki' + ('/_edit' if ext_url else ''),
                               rec.title)
            fileout.write('{url}\n'.format(url=url))

    # for page.
    page_recs = MWiki.query_all(limit=10000, kind='2')

    with open(file_name, 'a') as fileout:
        for rec in page_recs:
            url = os.path.join(SITE_CFG['site_url'],
                               'page' + ('/_edit' if ext_url else ''), rec.uid)

            fileout.write('{url}\n'.format(url=url))


def run_sitemap():
    '''
    Generate the sitemap file.
    '''
    site_map_file = 'xx_sitemap.txt'
    if os.path.exists(site_map_file):
        os.remove(site_map_file)

    gen_wiki_map(site_map_file)
    gen_post_map(site_map_file)


def run_editmap():
    '''
    Generate the urls file for editing.
    '''
    edit_map_file = 'xx_editmap.txt'
    if os.path.exists(edit_map_file):
        os.remove(edit_map_file)

    gen_wiki_map(edit_map_file, ext_url='_edit')
    gen_post_map(edit_map_file, ext_url='_edit')
