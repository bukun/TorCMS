# -*- coding:utf-8 -*-

'''
define the Core Modules of TorCMS.
'''

from torcms_metadata.modules import meta_modules

_modules = {

    'upload_excel': meta_modules.Upload_excel,
    'meta_catalog_of': meta_modules.MetaCategoryOf,
    'meta_recent': meta_modules.Meta_Recent,
    'meta_catalog': meta_modules.MetaCategory

}
