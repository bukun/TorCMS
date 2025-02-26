# -*- coding:utf-8 -*-

'''
User defined Configuration for the application.
'''

#Used by Django
DB_INFO =  {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": "torcms",
        "USER": "torcms",
        "PASSWORD": '111111',
        'HOST': '127.0.0.1',
        'CONN_MAX_AzGE': 7200,
    }

DB_CFG = {
    'host': DB_INFO['HOST'],
    'db': DB_INFO['NAME'],
    'user': DB_INFO['USER'],
    'pass': DB_INFO['PASSWORD'],
}

REDIS_CFG = {
    'host': '',
    'port': '',
    'pass': ''
}

SMTP_CFG = {
    'name': 'TorCMS',
    'host': "smtp.ym.163.com",
    'user': "admin@yunsuan.org",
    'pass': "",
    'postfix': 'yunsuan.org',
}

SITE_CFG = {
    'site_url': 'http://127.0.0.1:8888',
    'cookie_secret': '123456',
    'DEBUG': False
}

ROLE_CFG = {
    'add': '1000',
    'edit': '2000',
    'delete': '3000',
    'check': '0001', # 审核权限
}
