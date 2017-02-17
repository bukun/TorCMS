# -*- coding:utf-8 -*-

'''
Generate HTML for filter, included.
'''

import os

from torcms.script.autocrud.tpl import TPL_LISTINFO
# try:
#     import xxtmp_html_dic as html_vars
#     import xxtmp_array_add_edit_view as dic_vars
#     VAR_NAMES = dir(dic_vars)
# except ImportError:
#     pass

from torcms.script.autocrud.func_to_html_listinfo import *
from torcms.script.autocrud.base_crud import crud_path

from torcms.script.autocrud.fetch_html_dic import gen_html_dic
from torcms.script.autocrud.fetch_switch_dic import gen_array_crud

html_dics = gen_html_dic()
switch_dics, kind_dics = gen_array_crud()


def do_for_dir(html_tpl):
    '''
    doing for directory.
    :param html_tpl:
    :return:
    '''
    out_dir = os.path.join(os.getcwd(), crud_path, 'infolist')
    if os.path.exists(out_dir):
        pass
    else:
        os.mkdir(out_dir)
    # for var_name in VAR_NAMES:
    for var_name, bl_val in switch_dics.items():
        if var_name.startswith('dic_'):
            outfile = os.path.join(out_dir, 'infolist' + '_' + var_name.split('_')[1] + '.html')
            html_view_str_arr = []
            # tview_var = eval('dic_vars.' + var_name)
            tview_var = bl_val
            subdir = ''
            for x in tview_var:
                # sig = eval('html_vars.html_' + x)

                sig = html_dics['html_' + x]
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
                        kind_dics['kind_' + var_name.split('_')[-1]]
                        # eval('dic_vars.kind_' + var_name.split('_')[-1])
                    )
                )


def run_gen_listinfo():
    str_html_tpl = TPL_LISTINFO
    do_for_dir(str_html_tpl)
