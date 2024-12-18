from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import iga_group
from .resources import IgagroupResource
from django.db import models
from django.forms import TextInput, Textarea

class igagroupadmin(ImportExportModelAdmin):
    resource_class = IgagroupResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","title")
    list_per_page = 20

# 注册app的admin
admin.site.register(iga_group, igagroupadmin)
