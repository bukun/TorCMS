# -*- coding:utf-8 -*-

'''
define the Core Modules of TorCMS.
'''

from torcms_metadata_yml.modules import meta_modules

_modules = {
    'upload_excel': meta_modules.Upload_excel,
    'meta_catalog': meta_modules.MetaCategory,
}
