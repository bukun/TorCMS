from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import iga_room
from .resources import IgaroomResource
from django.db import models
from django.forms import TextInput, Textarea

class igaroomadmin(ImportExportModelAdmin):
    resource_class = IgaroomResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","title",'num','area','staff','building','floor')
    list_per_page = 20
    filter_horizontal = ('group', 'sites')
    readonly_fields = ('floor_num',)
# 注册app的admin
admin.site.register(iga_room, igaroomadmin)
