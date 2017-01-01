# -*- coding:utf-8 -*-
def gen_input_add(sig):
    html_fangjia = '''
<div class="form-group">
    <label class="col-sm-2 control-label" for="{0}"><span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;"></a> {1}</span></label>
<div class="col-sm-9">
    <input id='{0}' name="{0}" value="" type="text"  class="form-control">
     </div>
     <div class="col-sm-1">
     {2}
    </div>
    '''.format(sig['en'], sig['zh'], sig['dic'][1])
    return (html_fangjia)


def gen_input_edit(sig):
    edit_fangjia = '''
<div class="form-group">
    <label  class="col-sm-2 control-label"  for="{0}"><span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;"></a> {1}</span> </label>
<div class="col-sm-9">
    <input id='{0}' name="{0}" value="{{{{ post_info.extinfo['{0}'] if  '{0}' in post_info.extinfo else 0 }}}}" type="text"  class="input_text"> </div>
     <div class="col-sm-1">{2}</div>
    '''.format(sig['en'], sig['zh'], sig['dic'][1])
    return (edit_fangjia)


def gen_input_view(sig):
    out_str = '''
    <div class="col-sm-4"><span class="des">{1}</span></div>
    <div class="col-sm-8"><span class="val">{{{{ post_info.extinfo['{0}'] if  '{0}' in post_info.extinfo else 0 }}}} {2}</span></div>
    '''.format(sig['en'], sig['zh'], sig['dic'][1])
    return (out_str)


def gen_radio_add(sig):
    html_zuoxiang = '''

    <label for="{0}"><span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;"></a> {1}</span>
    '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
        <input id="{0}" name="{0}" type="radio" class="input_text" value="{1}">{2}
       '''.format(sig['en'], key, dic_tmp[key])
        html_zuoxiang += tmp_str

    html_zuoxiang += '''</label>'''
    return (html_zuoxiang)


def gen_radio_edit(sig):
    edit_zuoxiang = '''7
    <label  for="{0}"><span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;"></a> {1}</span>
    '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
        <input id="{0}" name="{0}" type="radio"  class="input_text" value="{1}"
        {{% if  '{0}' in post_info.extinfo and post_info.extinfo['{0}'] == '{1}' %}}
        checked
        {{% end %}}
        >{2} '''.format(sig['en'], key, dic_tmp[key])
        edit_zuoxiang += tmp_str

    edit_zuoxiang += '''</label>'''
    return (edit_zuoxiang)


def gen_radio_view(sig):
    view_zuoxiang = '''
    <div class="col-sm-4"><span class="des">{0}</span></div>
    <div class="col-sm-8">
    '''.format(sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
         <span class="input_text">
         {{% if  '{0}' in post_info.extinfo and post_info.extinfo['{0}'] == "{1}" %}}
         {2}
         {{% end %}}
         </span>
        '''.format(sig['en'], key, dic_tmp[key])
        view_zuoxiang += tmp_str

    view_zuoxiang += '''</div>'''
    return (view_zuoxiang)


def gen_checkbox_add(sig):
    html_wuneisheshi = '''

    <label  for="{0}"><span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;"></a> {1}</span>
    '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
        <input id="{0}" name="{0}" type="checkbox" class="input_text" value="{1}">{2}
        '''.format(sig['en'], key, dic_tmp[key])
        html_wuneisheshi += tmp_str

    html_wuneisheshi += '''</label>'''
    return (html_wuneisheshi)


def gen_checkbox_edit(sig):
    edit_wuneisheshi = '''

     <label  for="{0}"><span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;"></a> {1}</span>
     '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
         <input id="{0}" name="{0}" type="checkbox" class="input_text" value="{1}"
         {{% if "{1}" in post_info.extinfo["{0}"] %}}
         checked="checked"
         {{% end %}}
         >{2} '''.format(sig['en'], key, dic_tmp[key])
        edit_wuneisheshi += tmp_str

    edit_wuneisheshi += '''</label>'''
    return (edit_wuneisheshi)


def gen_checkbox_view(sig):
    view_zuoxiang = '''
    <div class="col-sm-4"><span class="des">{0}</span></div>
    <div class="col-sm-8">
    '''.format(sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
         <span>
         {{% if "{0}" in post_info.extinfo["{1}"] %}}
         {2}
         {{% end %}}
         </span>
         '''.format(key, sig['en'], dic_tmp[key])
        view_zuoxiang += tmp_str

    view_zuoxiang += '''</div>'''
    return (view_zuoxiang)


def gen_select_add(sig):
    html_jushi = '''<div class="form-group">
    <label for="{0}" class="col-sm-2 control-label"><span>
    <a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;"></a> {1}</span></label>
    <div class="col-sm-10"><select id="{0}" name="{0}" class="form-control">'''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']

    for key in dic_tmp.keys():
        tmp_str = '''<option value="{1}">{2}</option>'''.format(sig['en'], key, dic_tmp[key])
        html_jushi += tmp_str

    html_jushi += '''</select></div></div>'''
    return (html_jushi)


def gen_select_edit(sig):
    edit_jushi = '''
<div class="form-group">
   <label  for="{0}"  class="col-sm-2 control-label">
   <span class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;"></span> {1}</label>
    <div class="col-sm-10">
    <select id="{0}" name="{0}" class="form-control">
    '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''        
        <option value="{1}"
        {{% if  '{0}' in post_info.extinfo and post_info.extinfo["{0}"] == "{1}" %}}
        selected = "selected"
        {{% end %}}
        >{2}</option>
        '''.format(sig['en'], key, dic_tmp[key])
        edit_jushi += tmp_str

    edit_jushi += '''</select></div></div>'''
    return (edit_jushi)


def gen_select_view(sig):
    view_jushi = '''
    <div class="row">
    <div class="col-sm-4"><span class="des"><strong>{0}</strong></span></div>
    <div class="col-sm-8">
    '''.format(sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''

         {{% if '{0}' in post_info.extinfo %}}
          {{% set tmp_var = post_info.extinfo["{0}"] %}}
          {{% if tmp_var == "{1}" %}}
          {2}
          {{% end %}}
          {{% end %}}

         '''.format(sig['en'], key, dic_tmp[key])
        view_jushi += tmp_str

    view_jushi += '''</div></div>'''
    return (view_jushi)


def gen_file_add(sig):
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
    return (add_html)


def gen_file_view(sig):
    view_html = ''
    return (view_html)


def gen_file_edit(sig):
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
    return (view_html)
