# -*- coding:utf-8 -*-

'''
The router used in App.
'''

import router
import torcms.core.router

# from pathlib import Path
# inws  = Path('.')
# import torcms_metadata.router
# + torcms_metadata.router.urls

urls = router.urls + torcms.core.router.urls
