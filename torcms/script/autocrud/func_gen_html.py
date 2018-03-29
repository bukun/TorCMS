# -*- coding:utf-8 -*-

'''
The functions for generating add, edit, view HTML file.
for each item.
'''
from .html_tpl import HTML_TPL_DICT


def gen_input_add(sig_dic):
    '''
    Adding for HTML Input control.
    :param sig_dic:
    :return:
    '''
    if sig_dic['en'] == 'tag_file_download':
        html_str = HTML_TPL_DICT['input_add_download'].format(
            sig_en=sig_dic['en'],
            sig_zh=sig_dic['zh'],
            sig_dic=sig_dic['dic'][1],
            sig_type=sig_dic['type']
        )
    else:
        html_str = HTML_TPL_DICT['input_add'].format(
            sig_en=sig_dic['en'],
            sig_zh=sig_dic['zh'],
            sig_dic=sig_dic['dic'][1],
            sig_type=sig_dic['type']
        )
    return html_str


def gen_input_edit(sig_dic):
    '''
    Editing for HTML input control.
    :param sig_dic:
    :return:
    '''
    if sig_dic['en'] == 'tag_file_download':
        html_str = HTML_TPL_DICT['input_edit_download'].format(
            sig_en=sig_dic['en'],
            sig_zh=sig_dic['zh'],
            sig_dic=sig_dic['dic'][1],
            sig_type=sig_dic['type']
        )
    else:
        html_str = HTML_TPL_DICT['input_edit'].format(
            sig_en=sig_dic['en'],
            sig_zh=sig_dic['zh'],
            sig_dic=sig_dic['dic'][1],
            sig_type=sig_dic['type']
        )
    return html_str


def gen_input_view(sig_dic):
    '''
    Viewing the HTML text.
    '''
    if sig_dic['en'] == 'tag_file_download':
        html_str = HTML_TPL_DICT['input_view_download'].format(
            sig_zh=sig_dic['zh'],
            sig_unit=sig_dic['dic'][1]
        )
    elif sig_dic['en'] in ['tag_access_link', 'tag_dmoz_url',
                           'tag_online_link', 'tag_event_url',
                           'tag_expert_home', 'tag_pic_url']:
        # Todo: should do nothing with dmzo, expert, etc.
        html_str = HTML_TPL_DICT['input_view_link'].format(
            sig_dic['en'],
            sig_dic['zh'],
            sig_dic['dic'][1]
        )

    else:
        html_str = HTML_TPL_DICT['input_view'].format(
            sig_dic['en'],
            sig_dic['zh'],
            sig_dic['dic'][1]
        )
    return html_str


def gen_radio_add(sig_dic):
    '''
    Adding for HTML radio control.
    :param sig_dic:
    :return:
    '''
    # html_zuoxiang = '''
    # <label for="{0}"><span>
    # <a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;"></a> {1}</span>
    # '''.format(sig['en'], sig['zh'])

    # each item for radio.
    radio_control_str = ''
    dic_tmp = sig_dic['dic']
    for key, val in dic_tmp.items():
        tmp_str = '''
        <input id="{0}" name="{0}" type="radio" class="form-control" value="{1}">{2}
       '''.format(sig_dic['en'], key, val)
        radio_control_str += tmp_str

    # html_zuoxiang += '''</label>'''

    return '''<label for="{sig_en}"><span>
    <a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;">
    </a>{sig_zh}</span>
    {radio_str}</label>'''.format(sig_en=sig_dic['en'],
                                  sig_zh=sig_dic['zh'],
                                  radio_str=radio_control_str)


def gen_radio_edit(sig_dic):
    '''
    editing for HTML radio control.
    :param sig_dic:
    :return:
    '''
    edit_zuoxiang = '''7
    <label  for="{0}"><span>
    <a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;">
    </a>{1}</span>
    '''.format(sig_dic['en'], sig_dic['zh'])

    dic_tmp = sig_dic['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
        <input id="{0}" name="{0}" type="radio"  class="form-control" value="{1}"
        {{% if  '{0}' in postinfo.extinfo and postinfo.extinfo['{0}'] == '{1}' %}}
        checked
        {{% end %}}
        >{2} '''.format(sig_dic['en'], key, dic_tmp[key])
        edit_zuoxiang += tmp_str

    edit_zuoxiang += '''</label>'''
    return edit_zuoxiang


def gen_radio_view(sig_dic):
    '''
    for checkbox
    '''
    view_zuoxiang = '''
    <div class="col-sm-4"><span class="des">{0}</span></div>
    <div class="col-sm-8">
    '''.format(sig_dic['zh'])

    dic_tmp = sig_dic['dic']
    for key in dic_tmp.keys():
        tmp_str = '''<span class="input_text">
         {{% if  '{0}' in postinfo.extinfo and postinfo.extinfo['{0}'] == "{1}" %}}
         {2}
         {{% end %}}
         </span>'''.format(sig_dic['en'], key, dic_tmp[key])
        view_zuoxiang += tmp_str

    view_zuoxiang += '''</div>'''
    return view_zuoxiang


def gen_checkbox_add(sig_dic):
    '''
    for checkbox
    '''
    html_wuneisheshi = '''<label  for="{0}"><span>
    <a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;">
    </a>{1}</span>'''.format(sig_dic['en'], sig_dic['zh'])

    dic_tmp = sig_dic['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
        <input id="{0}" name="{0}" type="checkbox" class="form-control" value="{1}">{2}
        '''.format(sig_dic['en'], key, dic_tmp[key])
        html_wuneisheshi += tmp_str

    html_wuneisheshi += '''</label>'''
    return html_wuneisheshi


def gen_checkbox_edit(sig_dic):
    '''
    for checkbox
    '''
    edit_wuneisheshi = '''<label for="{0}"><span>
     <a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;">
     </a>{1}</span>
     '''.format(sig_dic['en'], sig_dic['zh'])

    dic_tmp = sig_dic['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
         <input id="{0}" name="{0}" type="checkbox" class="form-control" value="{1}"
         {{% if "{1}" in postinfo.extinfo["{0}"] %}}
         checked="checked"
         {{% end %}}
         >{2} '''.format(sig_dic['en'], key, dic_tmp[key])
        edit_wuneisheshi += tmp_str

    edit_wuneisheshi += '''</label>'''
    return edit_wuneisheshi


def gen_checkbox_view(sig_dic):
    '''
    for checkbox
    '''
    view_zuoxiang = '''
    <div class="col-sm-4"><span class="des">{0}</span></div>
    <div class="col-sm-8">
    '''.format(sig_dic['zh'])

    dic_tmp = sig_dic['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
         <span>
         {{% if "{0}" in postinfo.extinfo["{1}"] %}}
         {2}
         {{% end %}}
         </span>
         '''.format(key, sig_dic['en'], dic_tmp[key])
        view_zuoxiang += tmp_str

    view_zuoxiang += '''</div>'''
    return view_zuoxiang


def gen_select_add(sig_dic):
    '''
    Adding for select control.
    :param sig_dic:
        html_media_type = {
        'en': 'tag_media_type',
        'zh': 'Media_type',
        'dic': {1: 'Document', 2: 'Data', 3: 'Program'},
        'type': 'select',
        }
    :return:
    '''

    option_str = ''

    for key, val in sig_dic['dic'].items():
        tmp_str = '''<option value="{0}">{1}</option>'''.format(key, val)
        option_str += tmp_str

    return '''<div class="form-group">
    <label for="{sig_en}" class="col-sm-2 control-label"><span>
    <a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;"></a>
    {sig_zh}</span></label>
    <div class="col-sm-10"><select id="{sig_en}" name="{sig_en}" class="form-control">
    {option_str}</select></div></div>
    '''.format(sig_en=sig_dic['en'], sig_zh=sig_dic['zh'], option_str=option_str)


def gen_select_edit(sig_dic):
    '''
    Editing for select control.
    :param sig_dic:
    :return:
    '''

    option_str = ''
    for key, val in sig_dic['dic'].items():
        tmp_str = '''
        <option value="{1}"
        {{% if  '{0}' in postinfo.extinfo and postinfo.extinfo["{0}"] == "{1}" %}}
        selected = "selected"
        {{% end %}}
        >{2}</option>
        '''.format(sig_dic['en'], key, val)
        option_str += tmp_str

    return '''<div class="form-group">
    <label  for="{sig_en}"  class="col-sm-2 control-label">
    <span class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;">
    </span> {sig_zh}</label><div class="col-sm-10">
    <select id="{sig_en}" name="{sig_en}" class="form-control">
    {option_str}
    </select></div></div>
    '''.format(sig_en=sig_dic['en'], sig_zh=sig_dic['zh'], option_str=option_str)


def gen_select_view(sig_dic):
    '''
    HTML view, for selection.
    :param sig_dic:
    :return:
    '''
    option_str = ''
    dic_tmp = sig_dic['dic']
    for key, val in dic_tmp.items():
        tmp_str = '''
         {{% if '{sig_en}' in postinfo.extinfo %}}
          {{% set tmp_var = postinfo.extinfo["{sig_en}"] %}}
          {{% if tmp_var == "{sig_key}" %}}
          {sig_dic}
          {{% end %}}
          {{% end %}}
         '''.format(sig_en=sig_dic['en'], sig_key=key, sig_dic=val)
        option_str += tmp_str

    return '''
    <div class="row">
    <div class="col-sm-4"><span class="des"><strong>{sig_zh}</strong></span></div>
    <div class="col-sm-8">
    {option_str}
    </div></div>
    '''.format(sig_zh=sig_dic['zh'], option_str=option_str)


def gen_file_add(sig_dic):
    '''
    For adding file
    '''
    _ = sig_dic
    add_html = '''
    <div class="form-group">
    <label class="col-sm-2 control-label" for="dasf">上传图片：</label>
    <div id="dasf" class="col-sm-10"> png,jpg,gif,jpeg格式！大小不得超过500KB </div>
    </div>
    <div class="form-group" >
    <label for="mymps_img2" class="col-sm-2 control-label"> </label>
    <div id="mymps_img2" class="col-sm-10">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img1">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img2">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img3">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img4">
    </div>
    </div>
    '''
    return add_html


def gen_file_view(sig_dic):
    '''
    for file viewing.
    '''
    _ = sig_dic
    view_html = ''
    return view_html


def gen_file_edit(sig_dic):
    '''
    for editing file.
    '''
    _ = sig_dic
    view_html = '''
    <div class="form-group">
    <label for="dasf">上传图片：</label>
    <div id="dasf" class="col-sm-10"> png,jpg,gif,jpeg格式！大小不得超过500KB </div>
    </div>
    <div class="form-group">
    <label for="mymps_img2" class="col-sm-2 control-label"> </label>
    <div id="mymps_img2" class="col-sm-10">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img1">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img2">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img3">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img4">
    </div>
    </div>
    '''
    return view_html


def gen_input_list(sig_dic):
    '''
    For generating List view HTML file for INPUT.
    for each item.
    '''
    out_str = '''
    <div class="col-sm-4"><span class="des">{1}</span></div>
    <div class="col-sm-8">
    <span class="iga_pd_val">{{{{ postinfo.extinfo['{0}'][0] }}}} {2}</span>
    </div>
    '''.format(sig_dic['en'], sig_dic['zh'], sig_dic['dic'][1])
    return out_str


def gen_radio_list(sig_dic):
    '''
    For generating List view HTML file for RADIO.
    for each item.
    '''
    view_zuoxiang = '''<span class="iga_pd_val">'''

    dic_tmp = sig_dic['dic']
    for key in dic_tmp.keys():
        tmp_str = '''{{% if postinfo.extinfo['{0}'][0] == "{1}" %}} {2} {{% end %}}
        '''.format(sig_dic['en'], key, dic_tmp[key])
        view_zuoxiang += tmp_str

    view_zuoxiang += '''</span>'''
    return view_zuoxiang


def gen_checkbox_list(sig_dic):
    '''
    For generating List view HTML file for CHECKBOX.
    for each item.
    '''
    view_zuoxiang = '''<span class="iga_pd_val">'''

    dic_tmp = sig_dic['dic']
    for key in dic_tmp.keys():
        tmp_str = '''{{% if "{0}" in postinfo.extinfo["{1}"] %}} {2}  {{% end %}}
        '''.format(key, sig_dic['en'], dic_tmp[key])
        view_zuoxiang += tmp_str

    view_zuoxiang += '''</span>'''
    return view_zuoxiang


def gen_select_list(sig_dic):
    '''
    For generating List view HTML file for SELECT.
    for each item.
    '''
    view_jushi = '''<span class="label label-primary" style="margin-right:10px">'''

    dic_tmp = sig_dic['dic']
    for key in dic_tmp.keys():
        tmp_str = '''{{% if '{0}' in postinfo.extinfo and postinfo.extinfo["{0}"][0] == "{1}" %}}
         {2} {{% end %}}'''.format(sig_dic['en'], key, dic_tmp[key])
        view_jushi += tmp_str

    view_jushi += '''</span>'''
    return view_jushi
