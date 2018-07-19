# -*- coding:utf-8 -*-

'''
Tempaltes for CRUD.
'''

TPL_ADD = '''
    {% extends "../../tmpl_kkkk/tpl_add.html" %}

    {% block header %}
    <h1>{{ header_text }}</h1>
    {% end %}

    {% block extrainfo %}

    <div id="iga_add_rec_box">
    xxxxxx
    </div>
    {% end %}
    {% block footer %}
    <p>{{ footer_text }}</p>
    {% end %}'''

TPL_EDIT = '''
    {% extends "../../tmpl_kkkk/tpl_edit.html" %}

    {% block header %}
    <h1>{{ header_text }}</h1>
    {% end %}

    {% block extrainfo %}

    <div id="iga_edit_rec_box">
    xxxxxx
    </div>
    {% end %}
    {% block footer %}
    <p>{{ footer_text }}</p>
    {% end %}'''

TPL_LIST = '''
    {% extends "../../tmpl_kkkk/tpl_list.html" %}
    {% block header %}
    {{ header_text }}
    {% end %}
    {% block infoselect %}
    <div class="infoselect"> xxxxxx </div>
    {% end %}

    {% block infonav %}
    {% end %}

    {% block infolist %}
    <div class="list_house">
    <ul class="list-group">
    <span id="resultSpan"></span>

    </ul>
    </div>
    {% end %}
    {% block footer %}
    <p>{{ footer_text }}</p>
    {% end %}'''

TPL_LISTINFO = '''{% extends "../../tmpl_kkkk/tpl_listinfo.html" %}'''

TPL_VIEW = '''{% extends "../../tmpl_kkkk/tpl_viewssss.html" %}
    {% block header %}
    <h1>{{ header_text }}</h1>
    {% end %}

    {% block extrainfo %}

    <div id="iga_view_rec_box">
    xxxxxx
    </div>

    {% end %}

    {% block footer %}
    <p>{{ footer_text }}</p>
    {% end %}'''

HTML_INPUT_EDIT_DOWNLOAD = '''
    <div class="form-group">
        <label  class="col-sm-2 control-label"  for="{sig_en}">
        <span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;">
        </a>{sig_zh}</span>
        </label>
        <div class="col-sm-8">
        <input id='{sig_en}' name="{sig_en}"
        value="{{{{ postinfo.extinfo['{sig_en}'] if '{sig_en}' in postinfo.extinfo else '' }}}}"
        type="{sig_type}"  class="form-control"> </div>
         <div class="col-sm-2"><a href="/entry/add" target="_blank" class="btn btn-primary" role="button">Upload</a></div>
         </div>
        '''
HTML_INPUT_EDIT = '''
        <div class="form-group">
        <label  class="col-sm-2 control-label"  for="{sig_en}">
        <span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;">
        </a>{sig_zh}</span>
        </label>
        <div class="col-sm-9">
        <input id='{sig_en}' name="{sig_en}"
        value="{{{{ postinfo.extinfo['{sig_en}'] if '{sig_en}' in postinfo.extinfo else '' }}}}"
        type="{sig_type}"  class="form-control"> </div>
         <div class="col-sm-1">{sig_dic}</div>
         </div>
        '''

HTML_INPUT_ADD_DOWNLOAD = '''<div class="form-group">
<label class="col-sm-2 control-label" for="{sig_en}">
<span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;">
</a>{sig_zh}</span>
</label>
<div class="col-sm-8">
<input id='{sig_en}' name="{sig_en}" value="" type="{sig_type}"
class="form-control">
</div>
<div class="col-sm-2">
<a href="/entry/add" target="_blank" class="btn btn-primary" role="button">Upload</a>
</div></div>
'''
HTML_INPUT_ADD = '''
        <div class="form-group">
        <label class="col-sm-2 control-label" for="{sig_en}">
        <span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;">
        </a>{sig_zh}</span>
        </label>
        <div class="col-sm-9">
        <input id='{sig_en}' name="{sig_en}" value="" type="{sig_type}"
        class="form-control">
         </div>
         <div class="col-sm-1">
         {sig_dic}
        </div></div>
        '''

HTML_INPUT_VIEW_DONWLOAD = '''<div class="row">
    <div class="col-sm-4"><span class="des"><strong>{sig_zh}</strong></span></div>
    <div class="col-sm-8">

    {{% if userinfo %}}

    {{% if postinfo.extinfo.get('tag_file_download') %}}
    <a class="val btn-xs btn btn-primary" onclick="entity_down('{{{{postinfo.uid}}}}')"
     id="file_download" style="cursor: pointer; color:#fff">
     <span class="glyphicon glyphicon-download-alt"> Download</span>
     {sig_unit}</a>
     {{% else %}}
     <span class="glyphicon glyphicon-ban-circle" style="color:red"> Unavailable</span>
    {{% end %}}
      {{% else %}}
    <a href="/user/login">Please download after login, click to <span class="btn btn-primary btn-xs"> login in</span>. </a>
    {{% end %}}
     </div></div>
    '''

HTML_INPUT_VIEW_LINK = '''<div class="row">
    <div class="col-sm-4"><span class="des"><strong>{1}</strong></span></div>
    <div class="col-sm-8">
    <a class="val" target="_blank" href="{{{{ postinfo.extinfo['{0}'] if '{0}' in postinfo.extinfo else '' }}}}
     {2}" style="cursor: pointer; color:#069">
     {{{{ postinfo.extinfo['{0}'] if '{0}' in postinfo.extinfo else '' }}}}
     {2} </a></div></div>
    '''
HTML_INPUT_VIEW = '''<div class="row">
    <div class="col-sm-4"><span class="des"><strong>{1}</strong></span></div>
    <div class="col-sm-8">
    <span class="val">{{{{ postinfo.extinfo['{0}'] if '{0}' in postinfo.extinfo else '' }}}}
     {2}</span></div></div>
    '''
HTML_TPL_DICT = {
    'input_add': HTML_INPUT_ADD,
    'input_add_download': HTML_INPUT_ADD_DOWNLOAD,
    'input_edit_download': HTML_INPUT_EDIT_DOWNLOAD,
    'input_edit': HTML_INPUT_EDIT,
    'input_view_download': HTML_INPUT_VIEW_DONWLOAD,
    'input_view_link': HTML_INPUT_VIEW_LINK,
    'input_view': HTML_INPUT_VIEW,
}
