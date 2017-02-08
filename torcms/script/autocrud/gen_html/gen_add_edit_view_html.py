# -*- coding: utf-8
'''
Generate HTML for add, edit, view
'''
import os

try:
    import xxtmp_html_dic as html_vars
    import xxtmp_array_add_edit_view as dic_vars

    VAR_NAMES = dir(dic_vars)

except ImportError:
    pass

from torcms.script.autocrud.gen_html.func_to_html_add_edit_view import *
from torcms.script.autocrud.base_crud import crud_path
from torcms.script.autocrud.gen_html.tpl import tpl_add
from torcms.script.autocrud.gen_html.tpl import tpl_view
from torcms.script.autocrud.gen_html.tpl import tpl_edit

def gen_add_edit_view_tmpl():
    out_dir = os.path.join(os.getcwd(), crud_path)
    for bianliang in VAR_NAMES:
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
            var_dic = eval('dic_vars.' + bianliang)
            for sig in var_dic:
                html_sig = '_'.join(['html', sig])
                var_html = eval('html_vars.' + html_sig)
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
                    tpl_add.replace(
                        'xxxxxx',
                        ''.join(add_widget_arr)
                    ).replace(
                        'yyyyyy',
                        bianliang.split('_')[1][:2]
                    ).replace(
                        'ssssss', subdir
                    ).replace(
                        'kkkk',
                        eval('dic_vars.kind_' + bianliang.split('_')[-1])
                    )
                )

            view_widget_arr = []
            var_dic = eval('dic_vars.' + bianliang)
            for sig in var_dic:
                html_sig = '_'.join(['html', sig])
                var_html = eval('html_vars.' + html_sig)
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
                    tpl_view.replace(
                        'xxxxxx', ''.join(view_widget_arr)
                    ).replace(
                        'yyyyyy',
                        bianliang.split('_')[1][:2]
                    ).replace(
                        'ssssss',
                        subdir
                    ).replace(
                        'kkkk',
                        eval('dic_vars.kind_' + bianliang.split('_')[-1])
                    )
                )

            edit_widget_arr = []
            var_dic = eval('dic_vars.' + bianliang)
            for sig in var_dic:
                html_sig = '_'.join(['html', sig])
                var_html = eval('html_vars.' + html_sig)
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
                    tpl_edit.replace(
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
                        eval('dic_vars.kind_' + bianliang.split('_')[-1]))
                )
