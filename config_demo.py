# -*- coding:utf-8 -*-

from playhouse.postgres_ext import PostgresqlExtDatabase

menu_arr = [['首页', '/'],
            ['文档', '/category/geography'],
            ['云算', '/calc/find'],
            ['专题', '/spec/'],
            ]

page_num = 10

site_name = 'TorCMS网站'
site_url = 'http://127.0.0.1:8088'


cookie_secret = '12345'
redis_kw = 'lsadfkj'

smtp_cfg = {
    'name': 'TorCMS',
    'host': "smtp.ym.163.com",
    'user': "user_name@yunsuan.org",
    'pass': "password_here",
    'postfix': 'yunsuan.org',
}

PORT = '8088'

dbconnect = PostgresqlExtDatabase(
    'torcms',
    user='torcms',
    password='123456',
    host='127.0.0.1',
    autocommit=True,
    autorollback=True
)

app_url_name = 'map'

template_dir_name = 'templates'

torlite_template_name = 'tplite'
app_template_name = 'pycate'

lang = 'en_US'



cfg = {
    'info_per_page': 10,
    'debug': False,
}

router_post = {'1': 'post',
               '9': 'info',
               'm': 'map',
               }
