# -*- coding:utf-8
import os
try:
    from xxtmp_html_dic import *
    from xxtmp_array_add_edit_view import *
except:
    pass
from .base_crud import crud_path
from .tpl import tpl_list


def to_html(bl_str):
    bianliang = eval(bl_str)
    html_out = '''<li class="list-group-item">
    <div class="row"><div class="col-sm-3">{0}</div><div class="col-sm-9"> <span class="label label-default"  name='{1}' onclick='change(this);'  value=''>全部</span>
    '''.format(bianliang['zh'], bl_str.split('_')[1])

    tmp_dic = bianliang['dic']
    for key in tmp_dic.keys():
        tmp_str = '''<span  class="label label-default" name='{0}' onclick='change(this);' value='{1}'>{2}</span>
    '''.format('_'.join(bl_str.split('_')[1:]), key, tmp_dic[key])
        html_out += tmp_str
    html_out += '''</div></div></li>'''
    return (html_out)


def do_for_dir(html_tpl):
    var_names = globals().copy().keys()
    out_dir = os.path.join(os.getcwd(), crud_path, 'list')
    # out_dir = os.getcwd()
    if os.path.exists(out_dir):
        pass
    else:
        os.mkdir(out_dir)
    for var_name in var_names:
        if var_name.startswith('dic_'):
            # 根据父类，决定是否有子类。
            # if var_name.startswith('dic_a') and (not var_name.endswith('00')):
            #     subdir = 'tmpl{0}/'.format(var_name[-2:])
            # else:
            #     subdir = ''
            # 此处简化一下。
            subdir = ''
            outfile = os.path.join(out_dir, 'list' + '_' + var_name.split('_')[1] + '.html')
            html_view_str_arr = []
            tview_var = eval(var_name)
            for x in tview_var:
                sig = eval('html_' + x)
                if sig['type'] == 'select':
                    # html_view_str_arr.append(gen_select_view(sig))
                    html_view_str_arr.append(to_html('html_' + x))

            with open(outfile, 'w') as outfileo:
                outfileo.write(html_tpl.replace('xxxxxx', ''.join(html_view_str_arr)).replace('yyyyyy',
                                                                                              var_name.split('_')[1][:2]).replace(
                    'ssssss', subdir
                ).replace('kkkk', eval('kind_' + var_name.split('_')[-1]))
                               )

def do_list():
    str_html_tpl = tpl_list
    do_for_dir(str_html_tpl)
