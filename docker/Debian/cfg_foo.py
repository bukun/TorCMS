'''
User defined Configuration for the application.
'''

DB_CFG = {
    'host': '127.0.0.1',
    'db': 'torcms',
    'user': 'torcms',
    'pass': '111111',
    'port': 5555,
}

SMTP_CFG = {
    'name': 'TorCMS',
    'host': "smtp.ym.163.com",
    'user': "admin@torcms.com",
    'pass': "",
    'postfix': 'yunsuan.org',
}

SITE_CFG = {
    'site_url': 'http://127.0.0.1:8888',
    'cookie_secret': '123456',
    'DEBUG': True,
}

ROLE_CFG = {
    'add': '1000',
    'edit': '2000',
    'delete': '3000',
}
