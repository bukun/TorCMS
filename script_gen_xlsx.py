# -*- coding: utf-8


import os
import config
import pathlib
from openpyxl.reader.excel import load_workbook


def gen_xlsx_table():
    '''
    excel中的数据作为表中的字段，创建表
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
    fields = []
    for sheet_ranges in load_workbook(filename=XLSX_FILE):

        for xr in FILTER_COLUMNS:
            row1_val = sheet_ranges[xr + "1"].value
            row2_val = sheet_ranges[xr + "2"].value
            row3_val = sheet_ranges[xr + "3"].value
            row4_val = sheet_ranges[xr + "4"].value
            if row1_val and row1_val.strip() != '':
                desc = {
                    'slug': row1_val,
                    'name': row2_val,
                    'type': row3_val,
                    'display_mode': row4_val
                }

                fields.append(desc)

    create_tab(fields)


def create_tab(fields):
    stg_table_name = "ext_xlsx"
    columns = []
    primary_key = 'id'

    for field in fields:

        tags1 = [x.strip() for x in field['type'].split(':')]

        xx_1 = field['type'].split(':')

        if len(tags1) == 1:
            type = 'TEXT'
            unit = ''

        else:

            type = 'CHAR'

            if xx_1[1].isdigit():
                unit = xx_1[1]
            else:
                unit = ''

        if unit and type:
            table_column = field['slug'] + ' ' + type + '(' + unit + ')' + ',\n'
        else:
            table_column = field['slug'] + '  ' + type + ',\n'

        columns.append(table_column)


    # 创建数据表 #
    stg_create_columns = ''.join(columns)

    create_stg_sql = "create table %s (\n%sprimary key(%s)\n);" % (
        stg_table_name, stg_create_columns, primary_key)

    conn = config.DB_CON
    cur = conn.cursor()
    cur.execute(create_stg_sql)

    print("成功创建表格")

    conn.commit()
    conn.close()


if __name__ == '__main__':
    gen_xlsx_table()
