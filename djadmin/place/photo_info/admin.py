from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Photoinfo
from .resources import PhotoinfoResource

class photoinfoadmin(ImportExportModelAdmin):
    resource_class = PhotoinfoResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ( "title", "lat",  "lon")
    ordering = ["id"]
    list_per_page = 20



# 注册app的admin
admin.site.register(Photoinfo, photoinfoadmin)