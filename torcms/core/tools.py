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
from torcms.core.libs.deprecation import deprecated

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
    >>> check_username_valid('/sadf')
    False
    >>> check_username_valid('\s.adf')
    False
    '''
    if re.match('^[a-zA-Z][a-zA-Z0-9_]{3,19}', username) != None:
        return True
    return False


def check_email_valid(email_str):
    '''
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
    return hashlib.md5(instr.encode('utf-8')).hexdigest()


def timestamp():
    return int(time.time())


def format_yr(indate):
    return indate.strftime('%m-%d')


def format_date(indate):
    return indate.strftime('%Y-%m-%d %H:%M:%S')


def get_uuid():
    '''
    Using python uuid
    :return:
    '''
    return str(uuid.uuid1())


def get_uu8d():
    return str(uuid.uuid1()).split('-')[0]


def get_uu4d_v2():
    sel_arr = [x for x in 'ghijklmnopqrstuvwxyz']
    rarr = random.sample(sel_arr, 4)
    return ''.join(rarr)


def get_uu4d():
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    rarr = random.sample(sel_arr, 4)
    return ''.join(rarr)


def get_uu5d():
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    rarr = random.sample(sel_arr, 5)
    return ''.join(rarr)


def get_uudd(lenth):
    '''
    随机获取给定位数的整数
    :param lenth:
    :return:
    '''
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    rarr = random.sample(sel_arr, lenth)
    while rarr[0] == '0':
        rarr = random.sample(sel_arr, lenth)
    return int(''.join(rarr))


def get_uu6d():
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    rarr = random.sample(sel_arr, 6)
    return ''.join(rarr)


def markdown2html(markdown_text):
    html = markdown.markdown(markdown_text,
                             extensions=[WikiLinkExtension(base_url='/wiki/', end_url=''),
                                         'markdown.extensions.extra',
                                         'markdown.extensions.toc',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.meta', ])
    han_biaodians = ['。', '，', '；', '、', '！', '？']
    for han_biaodian in han_biaodians:
        html = html.replace(han_biaodian + '\n', han_biaodian)
    return tornado.escape.xhtml_escape(html)


@deprecated(details='using `tag_pager` as the replacement.')
def gen_pager_bootstrap_url(cat_slug, page_num, current):
    '''
    :return:
    '''
    if page_num == 1:
        return ''

    pager_shouye = '''<li class="{0}">
    <a href="{1}/{2}">&lt;&lt; 首页</a>
                </li>'''.format('hidden' if current <= 1 else '', cat_slug, current)

    pager_pre = '''                <li class="{0}">
                <a href="{1}/{2}">&lt; 前页</a>
                </li> '''.format('hidden' if current <= 1 else '', cat_slug, current - 1)
    pager_mid = ''
    for ind in range(0, page_num):
        tmp_mid = '''                <li class="{0}">
                <a  href="{1}/{2}">{2}</a></li>   '''.format('active' if ind + 1 == current else '',
                                                             cat_slug, ind + 1)
        pager_mid += tmp_mid
    pager_next = '''
                <li class=" {0}">
                <a  href="{1}/{2}">后页 &gt;</a>
                </li>'''.format('hidden' if current >= page_num else '', cat_slug, current + 1)
    pager_last = '''
                <li class=" {0}">
                <a href="{1}/{2}">末页
                    &gt;&gt;</a>
                </li>'''.format('hidden' if current >= page_num else '', cat_slug, page_num)
    pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
    return pager


@deprecated(details='using `tag_pager` as the replacement.')
def gen_pager_purecss(cat_slug, page_num, current):
    '''
    :return:
    '''
    if page_num == 1:
        return ''

    pager_shouye = '''
    <li class="pure-menu-item {0}">
    <a class="pure-menu-link" href="{1}">&lt;&lt; 首页</a>
                </li>'''.format('hidden' if current <= 1 else '', cat_slug)

    pager_pre = '''
                <li class="pure-menu-item {0}">
                <a class="pure-menu-link" href="{1}/{2}">&lt; 前页</a>
                </li> '''.format('hidden' if current <= 1 else '', cat_slug, current - 1)
    pager_mid = ''
    for ind in range(0, page_num):
        tmp_mid = '''
                <li class="pure-menu-item {0}">
                <a class="pure-menu-link" href="{1}/{2}">{2}</a></li>
                '''.format('selected' if ind + 1 == current else '', cat_slug, ind + 1)
        pager_mid += tmp_mid
    pager_next = '''
                <li class="pure-menu-item {0}">
                <a class="pure-menu-link" href="{1}/{2}">后页 &gt;</a>
                </li> '''.format('hidden' if current >= page_num else '', cat_slug, current + 1)
    pager_last = '''
                <li class="pure-menu-item {0}">
                <a hclass="pure-menu-link" ref="{1}/{2}">末页
                    &gt;&gt;</a>
                </li> '''.format('hidden' if current >= page_num else '', cat_slug, page_num)
    pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
    return pager


def average_array(num_arr):
    return sum(num_arr) / len(num_arr)


class ConfigDefault(object):
    SMTP_CFG = {
        'name': '地图画板',
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


def get_cfg():
    import cfg

    cfg_var = dir(cfg)

    if 'DB_CFG' in cfg_var:
        db_cfg = cfg.DB_CFG
    else:
        db_cfg = ConfigDefault.DB_CFG
    if 'user' not in db_cfg:
        db_cfg['user'] = db_cfg['db']

    if 'SMTP_CFG' in cfg_var:
        smtp_cfg = cfg.SMTP_CFG
    else:
        smtp_cfg = ConfigDefault.SMTP_CFG

    if 'SITE_CFG' in cfg_var:
        site_cfg = cfg.SITE_CFG
    else:
        site_cfg = ConfigDefault.SITE_CFG

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

    DB_CON = PostgresqlExtDatabase(
        db_cfg['db'],
        user=db_cfg['user'],
        password=db_cfg['pass'],
        host='127.0.0.1',
        autocommit=True,
        autorollback=True)

    return (DB_CON, smtp_cfg, site_cfg)
