# -*- coding:utf-8 -*-

import os
from .tpl import tpl_listinfo

try:
    from xxtmp_html_dic import *
    from xxtmp_array_add_edit_view import *
except:
    pass

from .func_to_html_listinfo import *
from .base_crud import crud_path


def do_for_dir(html_tpl):
    var_names = globals().copy().keys()
    out_dir = os.path.join(os.getcwd(), crud_path, 'infolist')
    if os.path.exists(out_dir):
        pass
    else:
        os.mkdir(out_dir)
    for var_name in var_names:
        if var_name.startswith('dic_'):
            outfile = os.path.join(out_dir, 'infolist' + '_' + var_name.split('_')[1] + '.html')
            html_view_str_arr = []
            tview_var = eval(var_name)
            subdir = ''
            for x in tview_var:
                sig = eval('html_' + x)
                if sig['type'] == 'select':
                    html_view_str_arr.append(gen_select_view(sig))
                elif sig['type'] == 'radio':
                    html_view_str_arr.append(gen_radio_view(sig))
                elif sig['type'] == 'checkbox':
                    html_view_str_arr.append(gen_checkbox_view(sig))

            with open(outfile, 'w') as outfileo:
                outfileo.write(html_tpl.replace('xxxxxx',
                                                ''.join(html_view_str_arr)).replace('yyyyyy',
                                                                                    var_name.split('_')[1][:2]).replace(
                    'ssssss', subdir
                ).replace('kkkk', eval('kind_' + var_name.split('_')[-1]))
                               )


def run_gen_listinfo():
    str_html_tpl = tpl_listinfo
    do_for_dir(str_html_tpl)
