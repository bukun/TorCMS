# -*- encoding:utf-8 -*-
'''
自动生成根据公式计算的APP
'''
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
from .arr_lisan import all_app

if os.path.exists('./templates/jshtml/1_auto/pyauto'):
    pass
else:
    os.makedirs('./templates/jshtml/1_auto/pyauto')


def gen_app(list_sig):
    all_list = all_app[list_sig]
    file_tmpl = ''.join(open(os.path.join(dir_path, 'tmpl.html')).readlines())
    tmpl = '''<div class="form-group">
                <label class="col-sm-2 control-label" for="{1}">{0}</label>
                <div class="col-sm-10">
                <select class="form-control" id="{1}" name="{1}" onchange='change("{1}")'>
                    {2}
                </select></div></div>'''
    tmpl_op = '''<option value="{0}">{1}</option>'''

    all_str = ''
    for alist in all_list:
        idx = 0

        select_str = ''
        for vv in alist['list']:
            tmpl_op_str = tmpl_op.format(idx, vv)
            select_str += tmpl_op_str
            idx += 1
        div_str = tmpl.format(alist['title'], alist['sig'], select_str)
        all_str += div_str

    js_list_str = ','.join(['"{0}"'.format(x['sig']) for x in all_list])
    outall_str = file_tmpl.format(js_list_str, all_str)

    with open('./templates/jshtml/1_auto/pyauto/{0}.html'.format(list_sig[4:]), 'w') as fo:
        fo.write(outall_str)


def run_gen_classed():
    for key in all_app.keys():
        if key.startswith('app_'):
            gen_app(key)
