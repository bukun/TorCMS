# -*- coding:utf-8

'''
Generate HTML for filter.
'''

import os
from torcms.script.autocrud.base_crud import crud_path
from torcms.script.autocrud.tpl import TPL_LIST

from torcms.script.autocrud.fetch_html_dic import gen_html_dic
from torcms.script.autocrud.fetch_switch_dic import gen_array_crud

html_dics = gen_html_dic()
switch_dics, kind_dics = gen_array_crud()


def to_html(bl_str):
    '''
    Convert to html.
    :param bl_str:
    :return:
    '''
    bianliang = html_dics[bl_str]
    # bianliang = eval('html_vars.' + bl_str)
    html_out = '''<li class="list-group-item">
    <div class="row"><div class="col-sm-3">{0}</div><div class="col-sm-9">
     <span class="label label-default"  name='{1}' onclick='change(this);' value=''>{{{{_('All')}}}}</span>
    '''.format(bianliang['zh'], '_'.join(bl_str.split('_')[1:]))

    tmp_dic = bianliang['dic']
    for key in tmp_dic.keys():
        tmp_str = '''
        <span  class="label label-default" name='{0}' onclick='change(this);' value='{1}'>
        {2}</span>'''.format('_'.join(bl_str.split('_')[1:]), key, tmp_dic[key])
        html_out += tmp_str
    html_out += '''</div></div></li>'''
    return html_out


def do_for_dir(html_tpl):
    '''
    doing for directory.
    :param html_tpl:
    :return:
    '''
    out_dir = os.path.join(os.getcwd(), crud_path, 'list')
    if os.path.exists(out_dir):
        pass
    else:
        os.mkdir(out_dir)
    # for var_name in VAR_NAMES:
    for var_name, bl_val in switch_dics.items():
        if var_name.startswith('dic_'):
            # 此处简化一下，不考虑子类的问题。
            subdir = ''
            outfile = os.path.join(out_dir, 'list' + '_' + var_name.split('_')[1] + '.html')
            html_view_str_arr = []
            # tview_var = eval('dic_vars.' + var_name)
            tview_var = bl_val
            for x in tview_var:
                # sig = eval('html_vars.html_' + x)
                sig = html_dics['html_' + x]
                if sig['type'] == 'select':
                    html_view_str_arr.append(to_html('html_' + x))

            with open(outfile, 'w') as outfileo:
                outfileo.write(html_tpl.replace(
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
                )
                    # eval('dic_vars.kind_' + var_name.split('_')[-1]))
                )


def do_list():
    do_for_dir(TPL_LIST)
