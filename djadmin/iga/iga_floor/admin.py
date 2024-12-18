from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import iga_floor
from .resources import IgafloorResource
from django.db import models
from django.forms import TextInput, Textarea

class igaflooradmin(ImportExportModelAdmin):
    resource_class = IgafloorResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","num")
    list_per_page = 20



# 注册app的admin
admin.site.register(iga_floor, igaflooradmin)
