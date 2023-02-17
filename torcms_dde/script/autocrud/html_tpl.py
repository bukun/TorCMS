# -*- coding:utf-8 -*-
'''
Tempaltes for CRUD.
'''

TPL_ADD = '''
    {% extends "../../../templates/tmpl_kkkk/tpl_addssss.html" %}

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
    {% extends "../../../templates/tmpl_kkkk/tpl_editssss.html" %}

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
    {% extends "../../../templates/tmpl_kkkk/tpl_list.html" %}
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

TPL_LISTINFO = '''{% extends "../../../templates/tmpl_kkkk/tpl_listinfo.html" %}'''

TPL_VIEW = '''{% extends "../../../templates/tmpl_kkkk/tpl_viewssss.html" %}
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

HTML_INPUT_EDIT = '''
 <div class="form-group">
<label  class="col-sm-2 control-label"  for="{sig_en}">
{{{{_('{sig_zh}')}}}}
</label>
<div class="col-sm-9">
<input id='{sig_en}' name="{sig_en}"
value="{{{{ postinfo.extinfo.get('{sig_en}','') }}}}"
type="text"  class="form-control"> </div> 
<div class="col-sm-1">{sig_dic}</div>
</div>
'''
HTML_INPUT_EDIT_hidden = '''
 
<input id='{sig_en}' name="{sig_en}"
value="{{{{ postinfo.extinfo.get('{sig_en}','') }}}}"
type="hidden"  class="form-control">  
'''
HTML_INPUT_ADD = '''
 <div class="form-group">
<label class="col-sm-2 control-label" for="{sig_en}">
{{{{_('{sig_zh}')}}}}
</label>
<div class="col-sm-9">
<input id='{sig_en}' name="{sig_en}" value="" type="text"
class="form-control">
</div>
<div class="col-sm-1">
{sig_dic}
</div>
 </div>
'''
HTML_INPUT_ADD_hidden = '''
 
<input id='{sig_en}' name="{sig_en}" value="" type="hidden"
class="form-control">
 
'''
HTML_INPUT_VIEW = '''{{% if postinfo.extinfo.get('{0}') and  postinfo.extinfo.get('{0}') not in ['',' ','None','NONE']  %}}<div class="row">
    <div class="col-sm-4"><span class="des"><strong>{{{{_('{1}')}}}}</strong></span></div>
    <div class="col-sm-8">
    <span class="val">{{{{ postinfo.extinfo.get('{0}','') }}}} {2}
     </span></div></div>{{% end %}}
    '''
HTML_INPUT_VIEW_link = '''{{% if postinfo.extinfo.get('{0}') and postinfo.extinfo.get('{0}') not in ['',' ','None','NONE']  %}}<div class="row">
    <div class="col-sm-4"><span class="des"><strong>{{{{_('{1}')}}}}</strong></span></div>
    <div class="col-sm-8">
    <span class="val">
    <a href="{{{{ postinfo.extinfo.get('{0}','') }}}}">{{{{ postinfo.extinfo.get('{0}','') }}}}</a>
     </span></div></div>{{% end %}}
    '''
HTML_INPUT_VIEW_DONWLOAD = '''<div class="row">
<div class="col-sm-4"><span class="des"><strong>{{{{_('{sig_zh}')}}}}</strong></span></div>
<div class="col-sm-8">

{{% if userinfo %}}

{{% if postinfo.extinfo.get('tag_file_download') or postinfo.extinfo.get('tag__file_download') %}}
<a class="val btn-xs btn btn-warning" onclick="entity_down('{{{{postinfo.uid}}}}')"
 id="file_download" style="cursor: pointer; color:#fff">
 <span class="glyphicon glyphicon-download-alt"> {{{{ _('Download') }}}}</span>
</a>
 {{% else %}}
 <span class="glyphicon glyphicon-ban-circle" style="color:red"> {{{{ _('Unavailable') }}}}</span>
{{% end %}}
  {{% else %}}
<a href="/user/login">{{{{ _('Please download after login, click to') }}}} <span class="btn btn-primary btn-xs"> {{{{ _('login in') }}}}</span>. </a>
{{% end %}}
 </div></div>
'''
HTML_INPUT_ADD_DOWNLOAD = ''' <div class="form-group">
<label class="col-sm-2 control-label" for="{sig_en}">
<span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;">
</a>{{{{_('{sig_zh}')}}}}</span>
</label>
<div class="col-sm-8">
<input id='ext_file' name="{sig_en}" value="" type="{sig_type}"
class="form-control">
</div>
<div class="col-sm-2">
   <a class="btn btn-primary btn-sm" data-toggle="modal" data-target="#myModal_file">
 {{{{ _('Upload File') }}}}
</a>
</div></div>
'''
HTML_INPUT_EDIT_DOWNLOAD = '''
 <div class="form-group">
<label  class="col-sm-2 control-label"  for="{sig_en}">
<span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;">
</a>{{{{_('{sig_zh}')}}}}</span>
</label>
<div class="col-sm-8">
<input id='ext_file' name="{sig_en}"
value="{{{{ postinfo.extinfo.get('{sig_en}','') }}}}"
type="{sig_type}"  class="form-control"> </div>
<div class="col-sm-2">  
 <a class="btn btn-primary btn-sm" data-toggle="modal" data-target="#myModal_file">
 {{{{ _('Upload File') }}}}
</a></div>
</div>
'''

HTML_TPL_DICT = {
    'input_add': HTML_INPUT_ADD,
    'input_add_hidden': HTML_INPUT_ADD_hidden,
    'input_edit': HTML_INPUT_EDIT,
    'input_edit_hidden': HTML_INPUT_EDIT_hidden,
    'input_view': HTML_INPUT_VIEW,
    'input_view_link': HTML_INPUT_VIEW_link,
    'input_add_download': HTML_INPUT_ADD_DOWNLOAD,
    'input_edit_download': HTML_INPUT_EDIT_DOWNLOAD,
    'input_view_download': HTML_INPUT_VIEW_DONWLOAD,
}
