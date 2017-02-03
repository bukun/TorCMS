# # -*- coding:utf-8 -*-
#
#
# from torcms.core import tools
# from torcms.model.core_tab import g_WikiHist
# from torcms.model.abc_model import Mabc
#
#
# class MPageHist(Mabc):
#     def __init__(self):
#         self.tab = g_WikiHist
#
#     def create_category(self, raw_data):
#
#         g_WikiHist.create(
#             uid=tools.get_uuid(),
#             title=raw_data.title,
#             wiki_id=raw_data.uid,
#             user_name=raw_data.user_name,
#             cnt_md=raw_data.cnt_md,
#             time_update=raw_data.time_update,
#
#             )
#         return True
