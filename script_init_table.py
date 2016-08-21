# -*- coding:utf-8 -*-


from torcms.model.core_tab import *

try:
    CabReply.create_table()
except:
    pass

try:
    CabPost2Reply.create_table()
except:
    pass

try:
    CabPage.create_table()
except:
    pass

try:
    CabLink.create_table()
except:
    pass



# uu = CabPost()
#
# members = [attr for attr in dir(CabPost())
#            if not callable(getattr(CabPost(), attr))
#            and not attr.startswith("_")]
#
# print(members)
#
# print('=' * 20)
# for kew in vars(CabPost):
#     print(kew)
