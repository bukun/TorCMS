'''

'''
import re
from cfg import DB_INFO
import psycopg2

import nltk
from nltk import data
import re

'''

'''

data.path.append("/home/dev/nltk_data/packages")
# data.path.append("/home/lihy/nltk_data/packages")

conn = psycopg2.connect(database=DB_INFO['NAME'], user=DB_INFO['USER'], password=DB_INFO['PASSWORD'],
                        host=DB_INFO['HOST'], port=DB_INFO['PORT'])

cursor = conn.cursor()


def check_prefix(string):
    pattern = r'^\d{1,2}\.\w+'  # 判断字符串的第一位到三位是否为数字加上点号。正则表达式模式，^表示开头，\d+表示至少1个数字，\.表示点号
    if re.match(pattern, string):

        return True
    else:
        return False


def join_line(incnts):
    out_arr = []
    sig_start = True
    sig_end = False
    tmp_str = ''
    indx = 0
    for cnt_q, cnt_h in zip([''] + incnts, incnts + ['\n']):
        # print('=' * 20)
        indx = indx + 1
        # print(indx)
        # print(cnt_q)
        # print(cnt_h)
        # print('is_end?', cnt_h == '\n')
        xx_cnt_q = cnt_q.strip()

        if len(xx_cnt_q) > 0 and xx_cnt_q[0] in ['#', '-', '*', '!', '`']:
            out_arr.append(cnt_q.lstrip())
            continue

        if len(xx_cnt_q) > 0 and check_prefix(xx_cnt_q[0]):
            out_arr.append(cnt_q.lstrip())
            continue

        if cnt_h == '\n':
            # print(indx)
            # print('-' * 20)
            # print(cnt_q)
            sig_end = True

            if tmp_str:
                out_arr.append(tmp_str + ' ' + cnt_q.strip())


            else:
                out_arr.append(cnt_q.strip())

            tmp_str = ''
            # print(sig_end)
            # print(tmp_str)
        else:
            if tmp_str:
                tmp_str = tmp_str + ' ' + cnt_q.strip()
            else:
                tmp_str = cnt_q.strip()
            sig_end = False
        # print('tmp_str:' , tmp_str)
        # print('sig_end: ', sig_end)
        if sig_end:
            out_arr.append('\n')

    result_arr = []
    for cnt in out_arr:
        if cnt == '\n':
            result_arr.append('\n')
        elif len(cnt) > 0 and cnt[0] in ['#']:
            result_arr.append('\n' + cnt + '\n')
        elif len(cnt) > 0 and cnt[0] in ['-', '*', '`']:
            result_arr.append(cnt)
        elif len(cnt) > 0 and cnt[0] in ['!']:
            result_arr.append('\n' + cnt.replace('\n', ''))
        elif len(cnt) > 0 and cnt[0].isdigit():
            result_arr.append(cnt)
        else:
            uu = nltk.sent_tokenize(cnt)
            result_arr.append('\n')
            for x in uu:
                result_arr.append(x + '\n')

    return result_arr


def update_db():
    query = "select id,cnt_md from crawldocumenten where state = 0 order by update_time desc "
    cursor.execute(query)

    recs = cursor.fetchall()

    for rec in recs:
        content = rec[1].splitlines()  # .split('\n')
        content = [f'{x}\n' for x in content]

        trans_con = join_line(content)
        all_con = ''.join(trans_con)
        sql = "UPDATE crawldocumenten SET cnt_md_edit = %s , state = 1 WHERE id = %s"
        values = (all_con, rec[0])
        cursor.execute(sql, values)
        conn.commit()
    print("已处理完成")


if __name__ == '__main__':
    update_db()
    # translate2()
