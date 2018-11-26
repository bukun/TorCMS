# -*- coding:utf-8 -*-
'''
Index for the application.
'''
import config
from torcms.core.base_handler import BaseHandler

from config import CMS_CFG


class ExtExcelHandler(BaseHandler):
    '''
    Index for the application.
    '''

    def initialize(self, **kwargs):
        super(ExtExcelHandler, self).initialize()

    def get(self, *args, **kwargs):
        if len(args) == 0 or args[0] == 'index':
            self.index()
        else:
            self.render('misc/html/404.html', kwd={}, userinfo=self.userinfo)

    def index(self):
        '''
        Index funtion.
        '''


        stg_table_name = 'ext_xlsx'
        conn = config.DB_CON
        cur = conn.cursor()
        select_stg_sql = "SELECT  *  from %s;" % (stg_table_name)
        cur.execute(select_stg_sql)

        recs = cur.fetchall()

        conn.close()

        self.render('ext_excel/index.html',
                    userinfo=self.userinfo,
                    recs = recs,
                    cfg=CMS_CFG,
                    kwd={}, )
