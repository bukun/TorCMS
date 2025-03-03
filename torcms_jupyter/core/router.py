# -*- coding:utf-8 -*-

from torcms_jupyter.handlers.jupyter_handler import JupyterHandler

_urls = [
    ('/jupyter/(.*)', JupyterHandler, dict(kind='j')),
]
