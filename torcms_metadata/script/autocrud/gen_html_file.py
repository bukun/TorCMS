'''
Generate HTML for add, edit, view

The type of the control inclusing `select`, text`, `digits`, ``date`, `number`, `email`, `url`.
The last 5 types is defined as in JQuery Validation.
'''

import os

# from htmlmin import minify
from . import func_gen_html
from .base_crud import CRUD_PATH, INPUT_ARR
from .fetch_html_dic import gen_array_crud, gen_array_crud_tag, gen_html_dic
from .html_tpl import TPL_ADD, TPL_EDIT, TPL_LIST, TPL_LISTINFO, TPL_VIEW

SWITCH_DICS_Meta = gen_array_crud()
OUT_DIR = os.path.join(os.getcwd(), CRUD_PATH)

HTML_DICS = gen_html_dic()

SWITCH_DICS, KIND_DICS = gen_array_crud_tag()
legend_html = ['''<legend>{{ _('Extra Metadata fields') }}</legend>''']


def minify(the_str):
    return the_str


def generate_html_files(*args):
    _ = args

    for tag_key, tag_list in SWITCH_DICS.items():
        if tag_key.startswith('dic_') and (not tag_key.endswith('00')):
            __write_add_tmpl(tag_key, tag_list)
            __write_edit_tmpl(tag_key, tag_list)
            __write_view_tmpl(tag_key, tag_list)

    __write_filter_tmpl(TPL_LIST)
    __write_list_tmpl(TPL_LISTINFO)


def __gen_select_filter(bl_str):
    '''
    Convert to html.
    :return String.
    '''
    bianliang = HTML_DICS[bl_str]
    # bianliang = eval('html_vars.' + bl_str)
    html_out = '''<li class="list-group-item">
    <div class="row"><div class="col-sm-3">{{{{_('{0}')}}}}</div><div class="col-sm-9">
     <span class="label label-default"  name='{1}' onclick='change(this);' value=''>{{{{_('All')}}}}</span>
    '''.format(bianliang['zh'], '_'.join(bl_str.split('_')[1:]))

    tmp_dic = bianliang['dic']
    for key in tmp_dic.keys():
        tmp_str = '''
        <span  class="label label-default" name='{0}' onclick='change(this);' value='{1}'>
        {{{{_('{2}')}}}}</span>'''.format('_'.join(bl_str.split('_')[1:]), key,
                                          tmp_dic[key])
        html_out += tmp_str
    html_out += '''</div></div></li>'''
    return html_out


def __write_edit_tmpl(tag_key, tag_list):
    '''
    Generate the HTML file for editing.
    :param tag_key: key of the tags.
    :param tag_list: list of the tags.
    :return: None
    '''
    edit_file = os.path.join(OUT_DIR, 'edit', 'edit.html')
    edit_widget_arr = []
    edit_widget_arr_meta = []
    for sig in tag_list:
        html_sig = '_'.join(['html', sig])
        # var_html = eval('html_vars.' + html_sig)
        var_html = HTML_DICS[html_sig]

        if var_html['type'] in INPUT_ARR:
            tmpl = func_gen_html.gen_input_edit(var_html)
        elif var_html['type'] == 'select':
            tmpl = func_gen_html.gen_select_edit(var_html)
        elif var_html['type'] == 'radio':
            tmpl = func_gen_html.gen_radio_edit(var_html)
        elif var_html['type'] == 'checkbox':
            tmpl = func_gen_html.gen_checkbox_edit(var_html)
        elif var_html['type'] == 'file':
            tmpl = func_gen_html.gen_file_edit(var_html)
        else:
            tmpl = ''
        edit_widget_arr.append(tmpl)

    for crud_dic in SWITCH_DICS_Meta:
        for crud_key, crud_val in crud_dic.items():
            tmpl_meta = func_gen_html.gen_input_edit_Meta(crud_key, crud_val)
            edit_widget_arr_meta.append(tmpl_meta)

    edit_widget_arr_all = edit_widget_arr_meta + legend_html + edit_widget_arr

    with open(edit_file, 'w') as fileout2:
        outstr = minify(TPL_EDIT.replace('xxxxxx', ''.join(edit_widget_arr_all)))
        fileout2.write(outstr)


def __write_view_tmpl(tag_key, tag_list):
    '''
    Generate the HTML file for viewing.
    :param tag_key: key of the tags.
    :param tag_list: list of the tags.
    :return: None
    '''
    view_file = os.path.join(OUT_DIR, 'view', 'view.html')
    view_widget_arr = []
    view_widget_arr_meta = []
    for sig in tag_list:
        html_sig = '_'.join(['html', sig])
        # var_html = eval('html_vars.' + html_sig)
        var_html = HTML_DICS[html_sig]

        if var_html['type'] in INPUT_ARR:
            tmpl = func_gen_html.gen_input_view(var_html)
        elif var_html['type'] == 'select':
            tmpl = func_gen_html.gen_select_view(var_html)
        elif var_html['type'] == 'radio':
            tmpl = func_gen_html.gen_radio_view(var_html)
        elif var_html['type'] == 'checkbox':
            tmpl = func_gen_html.gen_checkbox_view(var_html)
        elif var_html['type'] == 'file':
            tmpl = func_gen_html.gen_file_view(var_html)
        else:
            tmpl = ''

        # The admin information should be hidden for user.
        if sig.startswith('_'):
            tmpl = '''{% if userinfo and userinfo.role[1] > '0' %}''' + tmpl + '''{% end %}'''
        view_widget_arr.append(tmpl)

    for crud_dic in SWITCH_DICS_Meta:
        for crud_key, crud_val in crud_dic.items():
            tmpl_meta = func_gen_html.gen_input_view_Meta(crud_key, crud_val)
            view_widget_arr_meta.append(tmpl_meta)
    view_widget_arr_all = view_widget_arr_meta + view_widget_arr

    with open(view_file, 'w') as fileout:
        outstr = minify(TPL_VIEW.replace('xxxxxx', ''.join(view_widget_arr_all)))
        fileout.write(outstr)


def __write_add_tmpl(tag_key, tag_list):
    '''
    Generate the HTML file for adding.
    :param tag_key: key of the tags.
    :param tag_list: list of the tags.
    :return: None
    '''
    add_file = os.path.join(OUT_DIR, 'add',
                            'add.html')
    add_widget_arr = []
    add_widget_arr_meta = []
    # var_dic = eval('dic_vars.' + bianliang)
    for sig in tag_list:
        html_sig = '_'.join(['html', sig])
        # var_html = eval('html_vars.' + html_sig)
        var_html = HTML_DICS[html_sig]

        if var_html['type'] in INPUT_ARR:
            tmpl = func_gen_html.gen_input_add(var_html)
        elif var_html['type'] == 'select':
            tmpl = func_gen_html.gen_select_add(var_html)
        elif var_html['type'] == 'radio':
            tmpl = func_gen_html.gen_radio_add(var_html)
        elif var_html['type'] == 'checkbox':
            tmpl = func_gen_html.gen_checkbox_add(var_html)
        elif var_html['type'] == 'file':
            tmpl = func_gen_html.gen_file_add(var_html)
        else:
            tmpl = ''
        add_widget_arr.append(tmpl)

    for crud_dic in SWITCH_DICS_Meta:
        for crud_key, crud_val in crud_dic.items():
            tmpl_meta = func_gen_html.gen_input_add_Meta(crud_key, crud_val)
            add_widget_arr_meta.append(tmpl_meta)

    add_widget_arr_all = add_widget_arr_meta + legend_html + add_widget_arr

    with open(add_file, 'w') as fileout:
        outstr = minify(TPL_ADD.replace('xxxxxx', ''.join(add_widget_arr_all)))
        fileout.write(outstr)


def __write_filter_tmpl(html_tpl):
    '''
    doing for directory.
    '''
    out_dir = os.path.join(os.getcwd(), CRUD_PATH, 'list')
    if os.path.exists(out_dir):
        pass
    else:
        os.mkdir(out_dir)
    # for var_name in VAR_NAMES:
    for var_name, bl_val in SWITCH_DICS.items():
        if var_name.startswith('dic_'):
            # 此处简化一下，不考虑子类的问题。
            subdir = ''
            outfile = os.path.join(
                out_dir, 'list.html')
            html_view_str_arr = []
            # tview_var = eval('dic_vars.' + var_name)
            for the_val in bl_val:
                # sig = eval('html_vars.html_' + x)
                sig = HTML_DICS['html_' + the_val]
                if sig['type'] == 'select':
                    html_view_str_arr.append(
                        __gen_select_filter('html_' + the_val))

            with open(outfile, 'w') as outfileo:
                outstr = minify(html_tpl.replace('xxxxxx', ''.join(html_view_str_arr)))
                outfileo.write(outstr)


def __write_list_tmpl(html_tpl):
    '''
    doing for directory.
    '''
    out_dir = os.path.join(os.getcwd(), CRUD_PATH, 'infolist')
    if os.path.exists(out_dir):
        pass
    else:
        os.mkdir(out_dir)
    # for var_name in VAR_NAMES:
    for var_name, bl_val in SWITCH_DICS.items():
        if var_name.startswith('dic_'):
            outfile = os.path.join(
                out_dir, 'infolist.html')
            html_view_str_arr = []
            # tview_var = eval('dic_vars.' + var_name)
            subdir = ''
            for the_val2 in bl_val:
                # sig = eval('html_vars.html_' + x)

                sig = HTML_DICS['html_' + the_val2]
                if sig['type'] == 'select':
                    html_view_str_arr.append(
                        func_gen_html.gen_select_list(sig))
                elif sig['type'] == 'radio':
                    html_view_str_arr.append(func_gen_html.gen_radio_list(sig))
                elif sig['type'] == 'checkbox':
                    html_view_str_arr.append(
                        func_gen_html.gen_checkbox_list(sig))

            with open(outfile, 'w') as outfileo:
                outstr = minify(html_tpl.replace('xxxxxx', ''.join(html_view_str_arr)))
                outfileo.write(outstr)