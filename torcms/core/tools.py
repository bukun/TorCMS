# -*- coding:utf-8 -*-

'''
Some common function used by the CMS.
'''

import uuid
import random
import logging
import time
import hashlib
import re
from difflib import HtmlDiff
import markdown
from markdown.extensions.wikilinks import WikiLinkExtension
from playhouse.postgres_ext import PostgresqlExtDatabase
import tornado.escape

# try:
#     from jieba.analyse import ChineseAnalyzer
# except:
#     ChineseAnalyzer = None
# from whoosh.analysis import StemmingAnalyzer

from torcms.core.libs.deprecation import deprecated
import cfg
# import config

# Config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='xx_torcms.log',
                    filemode='w')
# 定义一个Handler打印INFO及以上级别的日志到sys.stderr
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
# 设置日志打印格式
logger_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
stream_handler.setFormatter(logger_formatter)
# 将定义好的console日志handler添加到root logger
logging.getLogger('').addHandler(stream_handler)

logger = logging


class Storage(dict):
    """
    from web.py
    对字典进行扩展，使其支持通过 dict.a形式访问以代替dict['a']
    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'


storage = Storage


def diff_table(rawinfo, newinfo):
    '''
    Generate the difference as the table format.
    :param rawinfo:
    :param newinfo:
    :return:
    '''
    return HtmlDiff.make_table(HtmlDiff(), rawinfo.split('\n'), newinfo.split('\n'),
                               context=True,
                               numlines=1)


def check_username_valid(username):
    '''
    Checking if the username if valid.

    >>> check_username_valid('/sadf')
    False
    >>> check_username_valid('\s.adf')
    False
    >>> check_username_valid('')
    False
    >>> check_username_valid(' ')
    False
    '''
    if re.match('^[a-zA-Z][a-zA-Z0-9_]{3,19}', username) != None:
        return True
    return False


def check_email_valid(email_str):
    '''
    Checking if the given Email is valid.

    >>> check_email_valid('')
    False
    >>> check_email_valid('s.adf')
    False
    >>> check_email_valid('sadfsdfa@comaldfsdaf.cosdafj')
    False
    '''
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",
                email_str) != None:
        return True

    return False


def md5(instr):
    '''
    md5
    '''
    return hashlib.md5(instr.encode('utf-8')).hexdigest()


def timestamp():
    '''
    The timestamp of integer.
    '''
    return int(time.time())


def format_yr(indate):
    '''
    date of yr
    '''
    return indate.strftime('%m-%d')


def format_date(indate):
    '''
    date of date
    '''
    return indate.strftime('%Y-%m-%d %H:%M:%S')


def get_uuid():
    '''
    Using python uuid
    :return:
    '''
    return str(uuid.uuid1())


def get_uu8d():
    '''
    Get ID of 8 digit.
    '''
    return str(uuid.uuid1()).split('-')[0]


func_rand_arr = lambda arr, len: ''.join(random.sample(arr, len))


def get_uu4d_v2():
    '''
    Get ID of 4 digit. version 2.
    '''
    sel_arr = [x for x in 'ghijklmnopqrstuvwxyz']
    return func_rand_arr(sel_arr, 4)


def get_uu4d():
    '''
    Get ID of 4 digit.
    '''
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    # rarr = random.sample(sel_arr, 4)
    return func_rand_arr(sel_arr, 4)


def get_uu5d():
    '''
    Get ID of 5 digit.
    '''
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    # rarr = random.sample(sel_arr, 5)
    return func_rand_arr(sel_arr, 5)


def get_uudd(lenth):
    '''
    随机获取给定位数的整数
    '''
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    rarr = random.sample(sel_arr, lenth)
    while rarr[0] == '0':
        rarr = random.sample(sel_arr, lenth)
    return int(''.join(rarr))


def get_uu6d():
    '''
    Get ID of 6 digit.
    '''
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    return func_rand_arr(sel_arr, 6)


def markdown2html(markdown_text):
    '''
    Convert markdown text to HTML. with extensions.
    :param markdown_text:   The markdown text.
    :return:  The HTML text.
    '''
    html = markdown.markdown(
        markdown_text,
        extensions=[
            WikiLinkExtension(base_url='/wiki/', end_url=''),
            'markdown.extensions.extra',
            'markdown.extensions.toc',
            'markdown.extensions.codehilite',
            'markdown.extensions.meta'
        ]
    )
    han_biaodians = ['。', '，', '；', '、', '！', '？']
    for han_biaodian in han_biaodians:
        html = html.replace(han_biaodian + '\n', han_biaodian)
    return tornado.escape.xhtml_escape(html)


@deprecated(details='using `tag_pager` as the replacement.')
def gen_pager_bootstrap_url(cat_slug, page_num, current):
    '''
    Generate the url.
    '''
    if page_num == 1:
        return ''

    pager_shouye = '''<li class="{0}"><a href="{1}/{2}">&lt;&lt; 首页</a></li>'''.format(
        'hidden' if current <= 1 else '',
        cat_slug,
        current
    )

    pager_pre = '''<li class="{0}"><a href="{1}/{2}">&lt; 前页</a></li>'''.format(
        'hidden' if current <= 1 else '',
        cat_slug,
        current - 1
    )
    pager_mid = ''
    for ind in range(0, page_num):
        tmp_mid = '''<li class="{0}"><a  href="{1}/{2}">{2}</a></li>'''.format(
            'active' if ind + 1 == current else '',
            cat_slug,
            ind + 1
        )
        pager_mid += tmp_mid
    pager_next = '''<li class=" {0}"><a  href="{1}/{2}">后页 &gt;</a></li>'''.format(
        'hidden' if current >= page_num else '',
        cat_slug,
        current + 1
    )
    pager_last = '''<li class=" {0}"><a href="{1}/{2}">末页&gt;&gt;</a></li>'''.format(
        'hidden' if current >= page_num else '',
        cat_slug,
        page_num
    )
    pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
    return pager


@deprecated(details='using `tag_pager` as the replacement.')
def gen_pager_purecss(cat_slug, page_num, current):
    '''
    :return:
    '''
    if page_num == 1:
        return ''

    pager_shouye = '''<li class="pure-menu-item {0}">
    <a class="pure-menu-link" href="{1}">&lt;&lt; 首页</a></li>'''.format(
        'hidden' if current <= 1 else '', cat_slug
    )

    pager_pre = '''<li class="pure-menu-item {0}">
                <a class="pure-menu-link" href="{1}/{2}">&lt; 前页</a>
                </li>'''.format('hidden' if current <= 1 else '',
                                cat_slug,
                                current - 1)
    pager_mid = ''
    for ind in range(0, page_num):
        tmp_mid = '''<li class="pure-menu-item {0}">
                <a class="pure-menu-link" href="{1}/{2}">{2}</a></li>
                '''.format('selected' if ind + 1 == current else '',
                           cat_slug,
                           ind + 1)
        pager_mid += tmp_mid
    pager_next = '''<li class="pure-menu-item {0}">
                <a class="pure-menu-link" href="{1}/{2}">后页 &gt;</a>
                </li> '''.format('hidden' if current >= page_num else '',
                                 cat_slug,
                                 current + 1)
    pager_last = '''<li class="pure-menu-item {0}">
                <a hclass="pure-menu-link" ref="{1}/{2}">末页
                &gt;&gt;</a>
                </li> '''.format('hidden' if current >= page_num else '',
                                 cat_slug,
                                 page_num)
    pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
    return pager


def average_array(num_arr):
    '''
    The average value of the given array.
    '''
    return sum(num_arr) / len(num_arr)


class ConfigDefault(object):
    '''
    Class for the default configuration.
    '''
    SMTP_CFG = {
        'name': 'TorCMS',
        'host': "",
        'user': "",
        'pass': "",
        'postfix': 'yunsuan.org',
    }

    SITE_CFG = {
        'site_url': 'http://127.0.0.1:8888',
        'cookie_secret': '123456',
        'DEBUG': False,
    }

    DB_CFG = {
        'db': 'travis_ci_torcms',
        'user': 'postgres',
        'pass': '',
    }

    ROLE_CFG = {
        'view': '',
        'add': '1000',
        'edit': '2000',
        'delete': '3000',
        'admin': '0300',
    }


# def get_analyzer():
#     '''
#     Get the analyzer for whoosh of difference language. Currrent only for zh and en.
#     '''
#     alyzer = {
#         'zh': ChineseAnalyzer,
#         'en': StemmingAnalyzer,
#     }
#
#     # cfg_var = dir(cfg)
#     # site_cfg = cfg.SITE_CFG if 'SITE_CFG' in cfg_var else ConfigDefault.SITE_CFG
#
#     site_cfg = config.SITE_CFG
#
#     site_cfg['LANG'] = site_cfg.get('LANG', 'zh')
#
#     if site_cfg['LANG'] == 'zh' and ChineseAnalyzer:
#         pass
#     else:
#         site_cfg['LANG'] = 'en'
#
#    print('x' * 20)
#    print(site_cfg)
#
#    # print(site_cfg['LANG'])
#    # return alyzer[site_cfg['LANG']]
#    return StemmingAnalyzer

def get_cfg():
    '''
    Get the configure value.
    '''

    cfg_var = dir(cfg)

    if 'DB_CFG' in cfg_var:
        db_cfg = cfg.DB_CFG
    else:
        db_cfg = ConfigDefault.DB_CFG

    if 'SMTP_CFG' in cfg_var:
        smtp_cfg = cfg.SMTP_CFG
    else:
        smtp_cfg = ConfigDefault.SMTP_CFG

    if 'SITE_CFG' in cfg_var:
        site_cfg = cfg.SITE_CFG
    else:
        site_cfg = ConfigDefault.SITE_CFG

    if 'ROLE_CFG' in cfg_var:
        role_cfg = cfg.ROLE_CFG
    else:
        role_cfg = ConfigDefault.ROLE_CFG

    role_cfg['view'] = role_cfg.get('view', '')
    role_cfg['add'] = role_cfg.get('add', '1000')
    role_cfg['edit'] = role_cfg.get('edit', '2000')
    role_cfg['delete'] = role_cfg.get('delete', '3000')
    role_cfg['admin'] = role_cfg.get('admin', '0300')

    ###################################################################

    site_url = site_cfg['site_url'].strip('/')
    site_cfg['site_url'] = site_url
    infor = site_url.split(':')
    if len(infor) == 1:
        site_cfg['PORT'] = 8888
    else:
        site_cfg['PORT'] = infor[-1]

    if 'DEBUG' in site_cfg:
        pass
    else:
        site_cfg['DEBUG'] = False

    db_con = PostgresqlExtDatabase(
        db_cfg['db'],
        user=db_cfg.get('user', db_cfg['db']),
        password=db_cfg['pass'],
        host='127.0.0.1',
        port=db_cfg.get('port', '5432'),
        autocommit=True,
        autorollback=True)

    return (db_con, smtp_cfg, site_cfg, role_cfg)
