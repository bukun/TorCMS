# -*- coding: utf-8 -*-

'''
Check the difference of modification.
'''
import os
import datetime

from torcms.core import tools
from torcms.model.post_model import MPost
from torcms.model.post_hist_model import MPostHist
from torcms.model.wiki_model import MWiki
from torcms.model.wiki_hist_model import MWikiHist
from torcms.core.tool.send_email import send_mail
from torcms.core.tools import diff_table
from config import SMTP_CFG, post_emails, SITE_CFG, router_post

now = datetime.datetime.now()

datestr = now.strftime('%Y-%m-%d %H:%M:%S')

time_limit = 7 * 60 * 60  # 每7小时


def get_diff_str(*args):
    mpost = MPost()
    mposthist = MPostHist()
    diff_str = ''

    for key in router_post.keys():
        recent_posts = mpost.query_recent_edited(tools.timestamp() - time_limit, kind=key)
        for recent_post in recent_posts:
            hist_rec = mposthist.get_last(recent_post.uid)
            if hist_rec:
                raw_title = hist_rec.title
                new_title = recent_post.title

                infobox = diff_table(raw_title, new_title)
                # infobox = test[start:end] + '</table>'
                # if ('diff_add' in infobox) or ('diff_chg' in infobox) or ('diff_sub' in infobox):
                diff_str = diff_str + '<h2 style="color:red; font-size:larger; font-weight:70;">TITLE: {0}</h2>'.format(
                    recent_post.title) + infobox

                infobox = diff_table(hist_rec.cnt_md, recent_post.cnt_md)

                diff_str = diff_str + '<h3>CONTENT:{0}</h3>'.format(
                    recent_post.title
                ) + infobox + '</hr>'
            else:
                continue
    return diff_str


def run_edit_diff(*args):
    email_cnt = '''<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title></title>
    <style type="text/css">
        table.diff {font-family:Courier; border:medium;}
        .diff_header {background-color:#e0e0e0}
        td.diff_header {text-align:right}
        .diff_next {background-color:#c0c0c0}
        .diff_add {background-color:#aaffaa}
        .diff_chg {background-color:#ffff77}
        .diff_sub {background-color:#ffaaaa}
    </style></head><body>'''

    idx = 1

    email_cnt = email_cnt + '<table border=1>'

    mpost = MPost()
    mposthist = MPostHist()

    for key in router_post.keys():
        recent_posts = mpost.query_recent_edited(tools.timestamp() - time_limit, kind=key)
        for recent_post in recent_posts:
            hist_rec = mposthist.get_last(recent_post.uid)
            if hist_rec:
                foo_str = '''
                    <tr><td>{0}</td><td>{1}</td><td class="diff_chg">Edit</td><td>{2}</td>
                    <td><a href="{3}">{3}</a></td></tr>
                    '''.format(idx, recent_post.user_name, recent_post.title,
                               os.path.join(SITE_CFG['site_url'], router_post[key], recent_post.uid))
                email_cnt = email_cnt + foo_str
            else:
                foo_str = '''
                    <tr><td>{0}</td><td>{1}</td><td class="diff_add">New </td><td>{2}</td>
                    <td><a href="{3}">{3}</a></td></tr>
                    '''.format(idx, recent_post.user_name, recent_post.title,
                               os.path.join(SITE_CFG['site_url'], router_post[key], recent_post.uid))
                email_cnt = email_cnt + foo_str
            idx = idx + 1

    ## wiki
    mpost = MWiki()
    mposthist = MWikiHist()

    recent_posts = mpost.query_recent_edited(tools.timestamp() - time_limit)
    for recent_post in recent_posts:
        hist_rec = mposthist.get_last(recent_post.uid)
        if hist_rec:
            foo_str = '''
                    <tr><td>{0}</td><td>{1}</td><td class="diff_chg">Edit</td><td>{2}</td>
                    <td><a href="{3}">{3}</a></td></tr>
                    '''.format(idx, recent_post.user_name, recent_post.title,
                               os.path.join(SITE_CFG['site_url'], 'wiki', recent_post.title))
            email_cnt = email_cnt + foo_str
        else:
            foo_str = '''
                    <tr><td>{0}</td><td>{1}</td><td class="diff_add">New </td><td>{2}</td>
                    <td><a href="{3}">{3}</a></td></tr>
                    '''.format(idx, recent_post.user_name, recent_post.title,
                               os.path.join(SITE_CFG['site_url'], 'wiki', recent_post.title))
            email_cnt = email_cnt + foo_str
        idx = idx + 1

    ## page.
    recent_posts = mpost.query_recent_edited(tools.timestamp() - time_limit, kind='2')
    for recent_post in recent_posts:
        hist_rec = mposthist.get_last(recent_post.uid)
        if hist_rec:
            foo_str = '''
                    <tr><td>{0}</td><td>{1}</td><td class="diff_chg">Edit</td><td>{2}</td>
                    <td><a href="{3}">{3}</a></td></tr>
                    '''.format(idx, recent_post.user_name, recent_post.title,
                               os.path.join(SITE_CFG['site_url'], 'page', recent_post.uid))
            email_cnt = email_cnt + foo_str
        else:
            foo_str = '''
                    <tr><td>{0}</td><td>{1}</td><td class="diff_add">New </td><td>{2}</td>
                    <td><a href="{3}">{3}</a></td></tr>
                    '''.format(idx, recent_post.user_name, recent_post.title,
                               os.path.join(SITE_CFG['site_url'], 'page', recent_post.uid))
            email_cnt = email_cnt + foo_str
        idx = idx + 1

    email_cnt = email_cnt + '</table>'

    ###########################################################

    diff_str = get_diff_str()

    if len(diff_str) < 20000:
        email_cnt = email_cnt + diff_str
    email_cnt = email_cnt + '''</body></html>'''

    if idx > 1:
        send_mail(post_emails, "{0}|{1}|{2}".format(SMTP_CFG['name'], '文档更新情况', datestr), email_cnt)
