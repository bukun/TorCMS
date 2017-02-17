# -*- coding: utf-8 -*-
'''
Generate HTML for add, edit, view
'''

import os

from torcms.script.autocrud.func_to_html_add_edit_view import *
from torcms.script.autocrud.base_crud import crud_path
from torcms.script.autocrud.tpl import TPL_ADD
from torcms.script.autocrud.tpl import TPL_VIEW
from torcms.script.autocrud.tpl import TPL_EDIT

from torcms.script.autocrud.fetch_html_dic import gen_html_dic
from torcms.script.autocrud.fetch_switch_dic import gen_array_crud

html_dics = gen_html_dic()
switch_dics, kind_dics = gen_array_crud()


def gen_add_edit_view_tmpl():
    out_dir = os.path.join(os.getcwd(), crud_path)
    for bianliang, bl_val in switch_dics.items():
        if bianliang.startswith('dic_') and (not bianliang.endswith('00')):
            # 根据父类，决定是否有子类。
            # 这里使用固定的值，类别id以"a"开头。
            if bianliang.startswith('dic_a'):
                subdir = 'sub{0}/'.format(bianliang[-2:])
            else:
                subdir = ''
            filesig = bianliang.split('_')[1]

            if bianliang.startswith('dic_a'):
                add_file = os.path.join(out_dir, 'add', 'add_' + filesig + '.html')
                edit_file = os.path.join(out_dir, 'edit', 'edit_' + filesig + '.html')
                view_file = os.path.join(out_dir, 'view', 'view_' + filesig + '.html')
            else:
                add_file = os.path.join(out_dir, 'add', 'add_' + filesig + '.html')
                edit_file = os.path.join(out_dir, 'edit', 'edit_' + filesig + '.html')
                view_file = os.path.join(out_dir, 'view', 'view_' + filesig + '.html')

            add_widget_arr = []
            # var_dic = eval('dic_vars.' + bianliang)
            var_dic = bl_val
            for sig in var_dic:
                html_sig = '_'.join(['html', sig])
                # var_html = eval('html_vars.' + html_sig)
                var_html = html_dics[html_sig]
                if var_html['type'] == 'text':
                    tmpl = (gen_input_add(var_html))
                if var_html['type'] == 'select':
                    tmpl = (gen_select_add(var_html))
                if var_html['type'] == 'radio':
                    tmpl = (gen_radio_add(var_html))
                if var_html['type'] == 'checkbox':
                    tmpl = (gen_checkbox_add(var_html))
                if var_html['type'] == 'file':
                    tmpl = (gen_file_add(var_html))
                add_widget_arr.append(tmpl)
            with open(add_file, 'w') as fo:
                fo.write(
                    TPL_ADD.replace(
                        'xxxxxx',
                        ''.join(add_widget_arr)
                    ).replace(
                        'yyyyyy',
                        bianliang.split('_')[1][:2]
                    ).replace(
                        'ssssss', subdir
                    ).replace(
                        'kkkk',
                        kind_dics['kind_' + bianliang.split('_')[-1]]
                        # eval('dic_vars.kind_' + bianliang.split('_')[-1])
                    )
                )

            view_widget_arr = []
            # var_dic = eval('dic_vars.' + bianliang)
            for sig in var_dic:
                html_sig = '_'.join(['html', sig])
                # var_html = eval('html_vars.' + html_sig)
                var_html = html_dics[html_sig]
                if var_html['type'] == 'text':
                    tmpl = (gen_input_view(var_html))
                if var_html['type'] == 'select':
                    tmpl = (gen_select_view(var_html))
                if var_html['type'] == 'radio':
                    tmpl = (gen_radio_view(var_html))
                if var_html['type'] == 'checkbox':
                    tmpl = (gen_checkbox_view(var_html))
                if var_html['type'] == 'file':
                    tmpl = (gen_file_view(var_html))
                view_widget_arr.append(tmpl)
            with open(view_file, 'w') as fo:
                fo.write(
                    TPL_VIEW.replace(
                        'xxxxxx', ''.join(view_widget_arr)
                    ).replace(
                        'yyyyyy',
                        bianliang.split('_')[1][:2]
                    ).replace(
                        'ssssss',
                        subdir
                    ).replace(
                        'kkkk',
                        kind_dics['kind_' + bianliang.split('_')[-1]]
                        # eval('dic_vars.kind_' + bianliang.split('_')[-1])
                    )
                )

            edit_widget_arr = []
            # var_dic = eval('dic_vars.' + bianliang)
            for sig in var_dic:
                html_sig = '_'.join(['html', sig])
                # var_html = eval('html_vars.' + html_sig)
                var_html = html_dics[html_sig]
                if var_html['type'] == 'text':
                    tmpl = (gen_input_edit(var_html))
                if var_html['type'] == 'select':
                    tmpl = (gen_select_edit(var_html))
                if var_html['type'] == 'radio':
                    tmpl = (gen_radio_edit(var_html))
                if var_html['type'] == 'checkbox':
                    tmpl = (gen_checkbox_edit(var_html))
                if var_html['type'] == 'file':
                    tmpl = (gen_file_edit(var_html))
                edit_widget_arr.append(tmpl)
            with open(edit_file, 'w') as fo:
                fo.write(
                    TPL_EDIT.replace(
                        'xxxxxx',
                        ''.join(edit_widget_arr)
                    ).replace(
                        'yyyyyy',
                        bianliang.split('_')[1][:2]
                    ).replace(
                        'ssssss',
                        subdir
                    ).replace(
                        'kkkk',
                        kind_dics['kind_' + bianliang.split('_')[-1]])
                    # eval('dic_vars.kind_' + bianliang.split('_')[-1]))
                )
