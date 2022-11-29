# -*- coding:utf-8 -*-

'''
The router used in App.
'''

import router
import torcms.core.router

from pathlib import Path
inws  = Path('.')

urls = router.urls + torcms.core.router.urls
for wdir in inws.iterdir():
    if wdir.is_dir() and wdir.name.startswith('torcms_'):
        the_file = f'{wdir.name}.core.router'
        _mod = __import__(the_file)
        urls = urls + _mod.core.router._urls
_urls = urls