# -*- coding: utf-8 -*-
'''
Check the difference of modification.
'''
import datetime
import os

from config import SITE_CFG, SMTP_CFG, post_emails, router_post
from torcms.core import tools
from torcms.core.tool.send_email import send_mail
from torcms.core.tools import diff_table
from torcms.model.comment_model import MComment
from torcms.model.post_hist_model import MPostHist
from torcms.model.post_model import MPost
from torcms.model.wiki_hist_model import MWikiHist
from torcms.model.wiki_model import MWiki

DATE_STR = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

TIME_LIMIT = 6 * 60 * 60 + 60  # Every 6 house, plus 60 seconds.


def __get_diff_recent():
    '''
    Generate the difference of posts. recently.
    '''
    diff_str = ''

    for key in router_post:
        recent_posts = MPost.query_recent_edited(tools.timestamp() -
                                                 TIME_LIMIT,
                                                 kind=key)
        for recent_post in recent_posts:
            hist_rec = MPostHist.get_last(recent_post.uid)
            if hist_rec:
                raw_title = hist_rec.title
                new_title = recent_post.title

                infobox = diff_table(raw_title, new_title)

                diff_str = diff_str + '''
                <h2 style="color:red;font-size:larger;font-weight:70;">TITLE: {0}</h2>
                '''.format(recent_post.title) + infobox

                infobox = diff_table(hist_rec.cnt_md, recent_post.cnt_md)

                diff_str = diff_str + '<h3>CONTENT:{0}</h3>'.format(
                    recent_post.title) + infobox + '</hr>'
            else:
                continue
    return diff_str


def __get_wiki_review(email_cnt, idx):
    '''
    Review for wikis.
    '''
    recent_posts = MWiki.query_recent_edited(tools.timestamp() - TIME_LIMIT,
                                             kind='2')
    for recent_post in recent_posts:
        hist_rec = MWikiHist.get_last(recent_post.uid)
        if hist_rec:
            foo_str = '''
                    <tr><td>{0}</td><td>{1}</td><td class="diff_chg">Edit</td><td>{2}</td>
                    <td><a href="{3}">{3}</a></td></tr>
                    '''.format(
                idx, recent_post.user_name, recent_post.title,
                os.path.join(SITE_CFG['site_url'], 'page', recent_post.uid))
            email_cnt = email_cnt + foo_str
        else:
            foo_str = '''
                    <tr><td>{0}</td><td>{1}</td><td class="diff_add">New </td><td>{2}</td>
                    <td><a href="{3}">{3}</a></td></tr>
                    '''.format(
                idx, recent_post.user_name, recent_post.title,
                os.path.join(SITE_CFG['site_url'], 'page', recent_post.uid))
            email_cnt = email_cnt + foo_str
        idx = idx + 1
    email_cnt = email_cnt + '</table>'
    return email_cnt, idx


def __get_page_review(email_cnt, idx):
    '''
    Review for pages.
    '''
    recent_posts = MWiki.query_recent_edited(tools.timestamp() - TIME_LIMIT)
    for recent_post in recent_posts:
        hist_rec = MWikiHist.get_last(recent_post.uid)
        if hist_rec:
            foo_str = '''
                    <tr><td>{0}</td><td>{1}</td><td class="diff_chg">Edit</td><td>{2}</td>
                    <td><a href="{3}">{3}</a></td></tr>
                    '''.format(
                idx, recent_post.user_name, recent_post.title,
                os.path.join(SITE_CFG['site_url'], 'wiki', recent_post.title))
            email_cnt = email_cnt + foo_str
        else:
            foo_str = '''
                    <tr><td>{0}</td><td>{1}</td><td class="diff_add">New </td><td>{2}</td>
                    <td><a href="{3}">{3}</a></td></tr>
                    '''.format(
                idx, recent_post.user_name, recent_post.title,
                os.path.join(SITE_CFG['site_url'], 'wiki', recent_post.title))
            email_cnt = email_cnt + foo_str
        idx = idx + 1

    return email_cnt, idx


def __get_post_review(email_cnt, idx):
    '''
    Review for posts.
    '''
    for key in router_post:
        recent_posts = MPost.query_recent_edited(tools.timestamp() -
                                                 TIME_LIMIT,
                                                 kind=key)
        for recent_post in recent_posts:
            hist_rec = MPostHist.get_last(recent_post.uid)
            editor_name = recent_post.extinfo.get('def_editor_name',
                                                  recent_post.user_name)
            if hist_rec:
                foo_str = ('<tr><td>{0}</td><td>{1}</td>'
                           '<td class="diff_chg">Edit</td>'
                           '<td>{2}</td><td><a href="{3}">{3}</a></td></tr>')
            else:
                foo_str = ('<tr><td>{0}</td><td>{1}</td>'
                           '<td class="diff_add">New </td>'
                           '<td>{2}</td><td><a href="{3}">{3}</a></td></tr>')

            foo_str = foo_str.format(
                idx, editor_name, recent_post.title,
                os.path.join(SITE_CFG['site_url'], router_post[key],
                             recent_post.uid))
            email_cnt = email_cnt + foo_str
            idx = idx + 1

    return email_cnt, idx


def __get_comment_list():
    '''
    Review for posts.
    '''

    idx = 1

    comment_cnt = '<br><br><table border=1><tr><td colspan=5><center><h3>有评论的信息列表<h3></center></td></tr>'
    recent_posts = MComment.query_recent_edited(tools.timestamp() - TIME_LIMIT)
    for recent_post in recent_posts:
        foo_str = ('<tr><td>{0}</td> '
                   '<td>{1}</td><td><a href="{2}">{2}</a></td></tr>')

        foo_str = foo_str.format(
            idx, recent_post.title,
            os.path.join(SITE_CFG['site_url'], router_post[recent_post.kind],
                         recent_post.uid))
        comment_cnt = comment_cnt + foo_str
        idx = idx + 1
    comment_cnt = comment_cnt + '''</table>'''
    return comment_cnt


def run_review(*args):
    '''
    Get the difference of recents modification, and send the Email.
    For: wiki, page, and post.
    '''
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

    email_cnt = email_cnt + '<table border=1><tr><td colspan=5><center><h3>文档更新情况<h3></center></td></tr>'

    email_cnt, idx = __get_post_review(email_cnt, idx)  # post
    email_cnt, idx = __get_page_review(email_cnt, idx)  # page.
    email_cnt, idx = __get_wiki_review(email_cnt, idx)  # wiki
    email_cnt = email_cnt + __get_comment_list()  # 有评论的信息列表

    ###########################################################

    diff_str = __get_diff_recent()

    if len(diff_str) < 20000:
        # 如果太多了，则不放在 Email 内容中.
        email_cnt = email_cnt + diff_str
    email_cnt = email_cnt + '''</body></html>'''

    if idx > 1:
        send_mail(post_emails, "{0}|{1}|{2}".format(SMTP_CFG['name'], '文档更新情况',
                                                    DATE_STR), email_cnt)
