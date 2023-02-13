# -*- coding:utf-8 -*-


from torcms.handlers.post_handler import PostHandler

_urls = [
    ("/tutorial/(.*)", PostHandler, dict(kind='k')),

]
