# -*- coding: utf-8 -*-

import config
from torcms.core import tools
from torcms.model.post_model import MPost
from torcms.model.post_hist_model import MPostHist
from torcms.model.wiki_model import MWiki
from torcms.model.wiki_hist_model import MWikiHist
from difflib import HtmlDiff
from torcms.core.tool.send_email import send_mail
from config import smtp_cfg
from config import site_url
from config_email import post_emails
import os
from torcms.core.tools import diff_table
import re

import datetime
from config import router_post

def run_sitemap():
    fo  = open('sitemap.txt', 'w')
    mpost = MPost()
    for key in router_post.keys():
        recent_posts = mpost.query_all(kind= key)
        for recent_post in recent_posts:
            url = 'http://www.osgeo.cn/{0}/{1}\n'.format(router_post[recent_post.kind], recent_post.uid)
            fo.write(url)
    ## wiki
    mpost = MWiki()
    recent_posts = mpost.query_all(limit_num=10000, kind='1')
    for recent_post in recent_posts:
        url = 'http://www.osgeo.cn/wiki/{0}\n'.format(recent_post.title)
        fo.write(url)

    ## page.
    recent_posts = mpost.query_all(limit_num=10000, kind='2')
    for recent_post in recent_posts:
        url = 'http://www.osgeo.cn/page/{0}\n'.format(recent_post.uid)
        fo.write(url)

