# -*- coding: utf-8 -*-
import getopt
import sys

from torcms.model.post_model import MPost
from torcms.script.script_init_tabels import create_table
from torcms_maplet.model.map_tab import MabGson, MabPost2Gson, MabLayout


def run_init():
    create_table(MabGson)
    create_table(MabLayout)
    create_table(MabPost2Gson)


def run_update_lon():
    '''
    :return:
    '''

    def fix_lon(lonval):
        return int(((lonval + 180) % 360 - 180) * 1000) / 1000

    map_recs = MPost.query_all(limit_num=5000, kind='2')
    for map_rec in map_recs:
        lon = float(map_rec.extinfo['ext_lon'])
        if lon > -180 and lon < 180:
            pass
        else:
            print('=' * 20)
            print(map_rec.uid)
            print(lon)
            out_dic = {'ext_lon': fix_lon(lon)}
            print(out_dic)
            MPost.update_jsonb(map_rec.uid, out_dic)


def entry(argv):
    try:
        # 这里的 h 就表示该选项无参数，i:表示 i 选项后需要有参数
        opts, args = getopt.getopt(argv, "hi:")
    except getopt.GetoptError:
        print('Error: helper.py -i cmd')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print('helper.py -i cmd')
            print('-' * 20)
            print('helper.py -i update_lon')
            sys.exit()
        elif opt in ("-i"):
            helper_app = arg
            eval('run_' + helper_app + '()')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('run:')
        print('    python helper_extor.py -h ')
        print('for help')
    else:
        entry(sys.argv[1:])
