# -*- coding:utf-8 -*-
from torcms.model.core_tab import g_Link
from torcms.model.supertable_model import MSuperTable


class MLink(MSuperTable):
    def __init__(self):
        self.tab = g_Link
        try:
            self.tab.create_table()
        except:
            pass

    def update(self, uid, post_data):
        entry = g_Link.update(
            name=post_data['name'],
            link=post_data['link'],
            order=post_data['order'],
            logo=post_data['logo'] if 'logo' in post_data else '',
        ).where(g_Link.uid == uid)
        entry.execute()

    def insert_data(self, id_link, post_data):
        uu = self.get_by_id(id_link)
        if uu:
            return (False)
        self.tab.create(
            name=post_data['name'],
            link=post_data['link'],
            order=post_data['order'],
            logo=post_data['logo'] if 'logo' in post_data else '',
            uid=id_link,
        )
        return (id_link)

    def query_link(self, num):
        return self.tab.select().limit(num).order_by(self.tab.order)
