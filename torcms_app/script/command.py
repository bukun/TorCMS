'''
Yunsuan中的工具，已经集成为：

helper_yunsuan.py -i check_jshtml
'''
import getopt
import os
import sys

from torcms.model.post_model import MPost
from torcms_app.script.autogen_convert.generate_classed import run_gen_classed
from torcms_app.script.autogen_formula.generate_app_html import run_gen_formula
from torcms_app.script.script_fix_app_path import run_fix_path


def run_gen_auto():
    '''
    生成自动
    '''
    run_gen_classed()
    run_gen_formula()


def run_check_jshtml(kind='s'):
    '''
    Check if the js path is correct.
    '''
    run_gen_auto()
    run_fix_path(kind=kind)
    print('=' * 20)

    js_recs = MPost.query_all(limit_num=10000, kind=kind)
    for js_rec in js_recs:
        os.path.join('./templates/jshtml', js_rec.extinfo['html_path'])
        if os.path.exists(os.path.join('./templates/jshtml', js_rec.extinfo['html_path'] + '.html')):
            pass
        else:
            print('Error: not found ' + js_rec.uid)


def entry(argv, kind='2'):
    try:
        # 这里的 h 就表示该选项无参数，i:表示 i 选项后需要有参数
        opts, args = getopt.getopt(argv, "hi:")
    except getopt.GetoptError:
        print('Error: helper.py -i cmd')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print('helper_yunsuan.py -i cmd')
            print('-' * 20)
            print('helper_yunsuan.py -i check_jshtml')
            sys.exit()
        elif opt in ("-i"):
            helper_app = arg
            eval('run_' + helper_app + '(kind = "{0}")'.format(kind))
