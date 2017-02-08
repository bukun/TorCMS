# -*- coding:utf-8 -*-

'''
Generate HTML for filter, included.
'''

import os

from torcms.script.autocrud.gen_html.tpl import tpl_listinfo

try:
    import xxtmp_html_dic as html_vars
    import xxtmp_array_add_edit_view as dic_vars
    VAR_NAMES = dir(dic_vars)
except ImportError:
    pass

from torcms.script.autocrud.gen_html.func_to_html_listinfo import *
from torcms.script.autocrud.base_crud import crud_path


def do_for_dir(html_tpl):
    out_dir = os.path.join(os.getcwd(), crud_path, 'infolist')
    if os.path.exists(out_dir):
        pass
    else:
        os.mkdir(out_dir)
    for var_name in VAR_NAMES:
        if var_name.startswith('dic_'):
            outfile = os.path.join(out_dir, 'infolist' + '_' + var_name.split('_')[1] + '.html')
            html_view_str_arr = []
            tview_var = eval('dic_vars.' + var_name)
            subdir = ''
            for x in tview_var:
                sig = eval('html_vars.html_' + x)
                if sig['type'] == 'select':
                    html_view_str_arr.append(gen_select_view(sig))
                elif sig['type'] == 'radio':
                    html_view_str_arr.append(gen_radio_view(sig))
                elif sig['type'] == 'checkbox':
                    html_view_str_arr.append(gen_checkbox_view(sig))

            with open(outfile, 'w') as outfileo:
                outfileo.write(
                    html_tpl.replace(
                        'xxxxxx',
                        ''.join(html_view_str_arr)
                    ).replace(
                        'yyyyyy',
                        var_name.split('_')[1][:2]
                    ).replace(
                        'ssssss',
                        subdir
                    ).replace(
                        'kkkk',
                        eval('dic_vars.kind_' + var_name.split('_')[-1])
                    )
                )


def run_gen_listinfo():
    str_html_tpl = tpl_listinfo
    do_for_dir(str_html_tpl)
