# -*- coding: utf-8 -*-
'''
Generate HTML for add, edit, view
'''

import os

from torcms.script.autocrud import func_to_html_add_edit_view
from .base_crud import crud_path
from .tpl import TPL_ADD, TPL_VIEW, TPL_EDIT
from .fetch_html_dic import gen_html_dic
from .fetch_switch_dic import gen_array_crud

HTML_DICS = gen_html_dic()
SWITCH_DICS, KIND_DICS = gen_array_crud()
OUT_DIR = os.path.join(os.getcwd(), crud_path)


def gen_add_edit_view_tmpl():
    '''
    Generate the templates for adding, editing, viewing.
    :return: None
    '''
    for tag_key, tag_list in SWITCH_DICS.items():
        if tag_key.startswith('dic_') and (not tag_key.endswith('00')):
            gen_add_tmpl(tag_key, tag_list)
            gen_view_tmpl(tag_key, tag_list)
            gen_edit_tmpl(tag_key, tag_list)


def gen_edit_tmpl(tag_key, tag_list):
    '''
    Generate the HTML file for editing.
    :param tag_key: key of the tags.
    :param tag_list: list of the tags.
    :return: None
    '''
    edit_file = os.path.join(OUT_DIR, 'edit', 'edit_' + tag_key.split('_')[1] + '.html')
    edit_widget_arr = []
    for sig in tag_list:
        html_sig = '_'.join(['html', sig])
        # var_html = eval('html_vars.' + html_sig)
        var_html = HTML_DICS[html_sig]
        if var_html['type'] == 'text':
            tmpl = func_to_html_add_edit_view.gen_input_edit(var_html)
        if var_html['type'] == 'select':
            tmpl = func_to_html_add_edit_view.gen_select_edit(var_html)
        if var_html['type'] == 'radio':
            tmpl = func_to_html_add_edit_view.gen_radio_edit(var_html)
        if var_html['type'] == 'checkbox':
            tmpl = func_to_html_add_edit_view.gen_checkbox_edit(var_html)
        if var_html['type'] == 'file':
            tmpl = func_to_html_add_edit_view.gen_file_edit(var_html)
        edit_widget_arr.append(tmpl)
    with open(edit_file, 'w') as fileout2:
        fileout2.write(
            TPL_EDIT.replace(
                'xxxxxx',
                ''.join(edit_widget_arr)
            ).replace(
                'yyyyyy',
                tag_key.split('_')[1][:2]
            ).replace(
                'kkkk',
                KIND_DICS['kind_' + tag_key.split('_')[-1]])
        )


def gen_view_tmpl(tag_key, tag_list):
    '''
    Generate the HTML file for viewing.
    :param tag_key: key of the tags.
    :param tag_list: list of the tags.
    :return: None
    '''
    view_file = os.path.join(OUT_DIR, 'view', 'view_' + tag_key.split('_')[1] + '.html')
    view_widget_arr = []
    for sig in tag_list:
        html_sig = '_'.join(['html', sig])
        # var_html = eval('html_vars.' + html_sig)
        var_html = HTML_DICS[html_sig]
        if var_html['type'] == 'text':
            tmpl = func_to_html_add_edit_view.gen_input_view(var_html)
        if var_html['type'] == 'select':
            tmpl = func_to_html_add_edit_view.gen_select_view(var_html)
        if var_html['type'] == 'radio':
            tmpl = func_to_html_add_edit_view.gen_radio_view(var_html)
        if var_html['type'] == 'checkbox':
            tmpl = func_to_html_add_edit_view.gen_checkbox_view(var_html)
        if var_html['type'] == 'file':
            tmpl = func_to_html_add_edit_view.gen_file_view(var_html)
        view_widget_arr.append(tmpl)
    the_view_sig_str = get_view_tmpl(tag_key)
    with open(view_file, 'w') as fileout:
        fileout.write(
            TPL_VIEW.replace(
                'xxxxxx', ''.join(view_widget_arr)
            ).replace(
                'yyyyyy',
                tag_key.split('_')[1][:2]
            ).replace(
                'ssss',
                the_view_sig_str
            ).replace(
                'kkkk',
                KIND_DICS['kind_' + tag_key.split('_')[-1]]
            )
        )
    return tmpl


def gen_add_tmpl(tag_key, tag_list):
    '''
    Generate the HTML file for adding.
    :param tag_key: key of the tags.
    :param tag_list: list of the tags.
    :return: None
    '''
    add_file = os.path.join(OUT_DIR, 'add', 'add_' + tag_key.split('_')[1] + '.html')
    add_widget_arr = []
    # var_dic = eval('dic_vars.' + bianliang)
    for sig in tag_list:
        html_sig = '_'.join(['html', sig])
        # var_html = eval('html_vars.' + html_sig)
        var_html = HTML_DICS[html_sig]
        if var_html['type'] == 'text':
            tmpl = func_to_html_add_edit_view.gen_input_add(var_html)
        if var_html['type'] == 'select':
            tmpl = func_to_html_add_edit_view.gen_select_add(var_html)
        if var_html['type'] == 'radio':
            tmpl = func_to_html_add_edit_view.gen_radio_add(var_html)
        if var_html['type'] == 'checkbox':
            tmpl = func_to_html_add_edit_view.gen_checkbox_add(var_html)
        if var_html['type'] == 'file':
            tmpl = func_to_html_add_edit_view.gen_file_add(var_html)
        add_widget_arr.append(tmpl)
    with open(add_file, 'w') as fileout:
        fileout.write(
            TPL_ADD.replace(
                'xxxxxx',
                ''.join(add_widget_arr)
            ).replace(
                'yyyyyy',
                tag_key.split('_')[1][:2]
            ).replace(
                'kkkk',
                KIND_DICS['kind_' + tag_key.split('_')[-1]]
            )
        )
    return tmpl


def get_view_tmpl(tag_key):
    '''
    根据分类uid的4位编码来找模板。如果4位的存在，则使用4位的；不然找其父类；再不然则使用通用模板
    只有View需要，edit, list使用通用模板
    '''
    the_view_file_4 = './templates/tmpl_{0}/tpl_view_{1}.html'.format(
        KIND_DICS['kind_' + tag_key.split('_')[-1]],
        tag_key.split('_')[1]
    )
    the_view_file_2 = './templates/tmpl_{0}/tpl_view_{1}.html'.format(
        KIND_DICS['kind_' + tag_key.split('_')[-1]],
        tag_key.split('_')[1][:2]
    )
    if os.path.exists(the_view_file_4):
        the_view_sig_str = '_{0}'.format(tag_key.split('_')[1])
    elif os.path.exists(the_view_file_2):
        the_view_sig_str = '_{0}'.format(tag_key.split('_')[1][:2])
    else:
        the_view_sig_str = ''
    return the_view_sig_str
