# -*- coding: utf-8


import os
import config
from openpyxl.reader.excel import load_workbook


def gen_xlsx_table_info():
    '''
    向表中插入数据
    '''

    XLSX_FILE = './database/meta/20180811.xlsx'
    if os.path.exists(XLSX_FILE):
        pass
    else:
        return

    RAW_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    FILTER_COLUMNS = RAW_LIST + ["A" + x for x in RAW_LIST] + \
                     ["B" + x for x in RAW_LIST] + \
                     ["C" + x for x in RAW_LIST] + \
                     ["D" + x for x in RAW_LIST]


    tvalue = []
    for sheet_ranges in load_workbook(filename=XLSX_FILE):


        for row_num in range(6,262):
            tvalue = []
            for xr in FILTER_COLUMNS:

                row1_val = sheet_ranges[xr + '1'].value
                row4_val = sheet_ranges[xr + '{0}'.format(row_num)].value

                if row1_val:
                    if row4_val == None:
                        row4_val =''
                    tvalue.append(row4_val)

            insert_tab(tvalue)



def insert_tab(tvalue):

    ttvalue = str(tvalue)[1:-1]
    stg_table_name = 'ext_xlsx'

    insert_stg_sql = "INSERT INTO %s VALUES (\n%s );" % (stg_table_name, ttvalue)


    conn = config.DB_CON
    cur = conn.cursor()
    cur.execute(insert_stg_sql)

    print("成功插入数据")

    conn.commit()
    conn.close()




if __name__ == '__main__':
    gen_xlsx_table_info()
