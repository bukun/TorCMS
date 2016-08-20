__author__ = 'bukun'

import sys


from torcms.model.mcatalog import MCatalog
from torcms.model.mappcatalog import MAppCatalog
from torcms.model.app_model import MApp

if __name__ == '__main__':

    mappcat = MAppCatalog()
    mapp = MApp()
    for rec in mappcat.query_all():
        uid= rec.uid
        uuvv = mapp.query_extinfo_by_cat(uid)
        print(uid, uuvv.count())
        mappcat.update_count(uid, uuvv.count())