# -*- coding:utf-8 -*-

'''
Tempaltes for CRUD.
'''

TPL_ADD = '''
    {% extends "../../tmpl_kkkk/tmplyyyyyy/sssssstpl_add.html" %}

    {% block topmenu %}
    {% raw topmenu %}
    {% end %}

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
    {% extends "../../tmpl_kkkk/tmplyyyyyy/sssssstpl_edit.html" %}

    {% block topmenu %}
    {% raw topmenu %}
    {% end %}

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
    {% extends "../../tmpl_kkkk/tmplyyyyyy/sssssstpl_list.html" %}
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

TPL_LISTINFO = '''{% extends "../../tmpl_kkkk/tmplyyyyyy/sssssstpl_listinfo.html" %}'''

TPL_VIEW = '''{% extends "../../tmpl_kkkk/tmplyyyyyy/sssssstpl_view.html" %}
    {% block topmenu %}
    {% raw topmenu %}
    {% end %}

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
