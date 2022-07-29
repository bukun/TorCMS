# -*- coding:utf-8 -*-
'''
Some common function used by the CMS.
'''

import hashlib
import logging
import random
import re
import time
import uuid
from difflib import HtmlDiff

import markdown
import tornado.escape
from htmlmin import minify
from markdown.extensions.wikilinks import WikiLinkExtension
from playhouse.postgres_ext import PostgresqlExtDatabase

import cfg

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='xx_torcms.log',
    filemode='w')
# 定义一个Handler打印INFO及以上级别的日志到sys.stderr
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
# 设置日志打印格式
logger_formatter = logging.Formatter(
    '%(name)-12s: %(levelname)-8s %(message)s')
stream_handler.setFormatter(logger_formatter)
# 将定义好的console日志handler添加到root logger
logging.getLogger('').addHandler(stream_handler)

logger = logging


def html_min(func):
    '''
    used as decorator to minify HTML string.
    Unused.
    '''

    def wrapper(*args):
        return minify(func(*args))

    return wrapper


def diff_table(rawinfo, newinfo):
    '''
    Generate the difference as the table format.
    :param rawinfo:
    :param newinfo:
    :return:
    '''
    return HtmlDiff.make_table(HtmlDiff(),
                               rawinfo.split('\n'),
                               newinfo.split('\n'),
                               context=True,
                               numlines=1)


def check_username_valid(username):
    '''
    Checking if the username if valid.

    >>> check_username_valid('/sadf')
    False
    >>> check_username_valid('\\s.adf')
    False
    >>> check_username_valid('')
    False
    >>> check_username_valid(' ')
    False
    '''
    if re.match('^[a-zA-Z][a-zA-Z0-9_]{3,19}', username) is not None:
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
    ck_str = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"
    if re.match(ck_str, email_str) is not None:
        return True

    return False


def check_pass_valid(pass_str):
    '''
    Checking if the given password is valid.
    至少6-20个字符，至少1个大写字母，1个小写字母和1个数字，其他可以是任意字符
    '''

    ck_str = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d][\s\S]{6,20}$"
    if re.match(ck_str, pass_str) is not None:
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
    '''
    return str(uuid.uuid1())


def get_uu8d():
    '''
    Get ID of 8 digit.
    '''

    # str(uuid.uuid1()).split('-', maxsplit=1)[0]
    return str(uuid.uuid1()).split('-', maxsplit=1)[0]


def func_rand_arr(arr, length):
    '''
    func_rand_arr = lambda arr, len: ''.join(random.sample(arr, len))
    '''
    return ''.join(random.sample(arr, length))


def get_uu4d_v2():
    '''
    Get ID of 4 digit. version 2.
    '''
    # sel_arr = [x for x in 'ghijklmnopqrstuvwxyz']

    return func_rand_arr(
        list('ghijklmnopqrstuvwxyz'),
        4
    )


def get_uu4d():
    '''
    Get ID of 4 digit.
    '''

    return func_rand_arr(
        list('0123456789abcdef'),
        4
    )


def get_uu5d():
    '''
    Get ID of 5 digit.
    '''

    return func_rand_arr(
        list('0123456789abcdef'),
        5
    )


def get_uudd(lenth):
    '''
    随机获取给定位数的整数
    '''
    sel_arr = list('0123456789')
    rarr = random.sample(sel_arr, lenth)
    while rarr[0] == '0':
        rarr = random.sample(sel_arr, lenth)
    return int(''.join(rarr))


def get_uu6d():
    '''
    Get ID of 6 digit.
    '''

    return func_rand_arr(
        list('0123456789abcdef'),
        6
    )


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


class ConfigDefault(object):
    '''
    Class for the default configuration.

    ``DB_CFG`` 的配置：这个是用于 Travis 。如果没有配置，则使用 Travis 的设置。
    一般应用中都是要进行配置的。
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

    # 权限的缺省值
    ROLE_CFG = {
        'view': '',
        'add': '1000',
        'edit': '2000',
        'delete': '3000',
        'admin': '0300',
    }


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

    db_con = PostgresqlExtDatabase(db_cfg['db'],
                                   user=db_cfg.get('user', db_cfg['db']),
                                   password=db_cfg['pass'],
                                   host=db_cfg.get('host', '127.0.0.1'),
                                   port=db_cfg.get('port', '5432'),
                                   # autocommit=True,
                                   autorollback=True)

    if 'REDIS_CFG' in cfg_var:
        redis_cfg = cfg.REDIS_CFG
        if not redis_cfg.get('host'):
            redis_cfg['host'] = 'localhost'
        if not redis_cfg.get('port'):
            redis_cfg['port'] = 6379
        if not redis_cfg.get('pass'):
            redis_cfg['pass'] = None
    else:
        redis_cfg = {'host': 'localhost', 'port': 6379, 'pass': None}

    return (db_con, smtp_cfg, site_cfg, role_cfg, redis_cfg)


def ts_helper():
    the_timestamp = int(time.time())
    ts1d = the_timestamp - 24 * 60 * 60
    ts7d = the_timestamp - 7 * 24 * 60 * 60
    ts30d = the_timestamp - 30 * 24 * 60 * 60
    return [x * 1000 for x in (ts1d, ts7d, ts30d)]
