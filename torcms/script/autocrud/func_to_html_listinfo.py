# -*- coding:utf-8 -*-

def gen_input_view(sig):
    out_str = '''
    <div class="col-sm-4"><span class="des">{1}</span></div>
    <div class="col-sm-8"><span class="iga_pd_val">{{{{ post_info.extinfo['{0}'][0] }}}} {2}</span></div>
    '''.format(sig['en'], sig['zh'], sig['dic'][1])
    return (out_str)


def gen_radio_view(sig):
    view_zuoxiang = '''<span class="iga_pd_val">    '''

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''{{% if post_info.extinfo['{0}'][0] == "{1}" %}} {2} {{% end %}}'''.format(sig['en'], key,
                                                                                               dic_tmp[key])
        view_zuoxiang += tmp_str

    view_zuoxiang += '''</span>'''
    return (view_zuoxiang)


def gen_checkbox_view(sig):
    view_zuoxiang = ''' <span class="iga_pd_val">    '''

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''{{% if "{0}" in post_info.extinfo["{1}"] %}} {2}  {{% end %}}'''.format(key, sig['en'],
                                                                                             dic_tmp[key])
        view_zuoxiang += tmp_str

    view_zuoxiang += '''</span>'''
    return (view_zuoxiang)


def gen_select_view(sig):
    view_jushi = '''<span class="label label-primary" style="margin-right:10px">    '''

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = ''' {{% if '{0}' in postinfo.extinfo and post_info.extinfo["{0}"][0] == "{1}" %}} {2} {{% end %}} '''.format(
            sig['en'], key, dic_tmp[key])
        view_jushi += tmp_str

    view_jushi += '''</span>'''
    return (view_jushi)
