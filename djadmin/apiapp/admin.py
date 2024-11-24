from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import apiapp
from .resources import ApiAppResource

class apiappadmin(ImportExportModelAdmin):
    resource_class = ApiAppResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = (
       "title", "cnt_md","create_time")
    # 用来排序
    ordering = ["app_id", "create_time",]
    list_per_page = 20

    search_fields = ('title', 'cnt_md')

    # filter_horizontal = ('label',)


# 注册app的admin
admin.site.register(apiapp, apiappadmin)
