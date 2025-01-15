from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from ..igais_category.models import igaisdata
from .resources import IgaisDataResource
from django.db import models
from django.forms import TextInput, Textarea
class igaisdataadmin(ImportExportModelAdmin):
    resource_class = IgaisDataResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = (
        "id","title", "cnt_md", "category", "user", "file", "view_count", "create_time","update_time",)
    # 用来排序
    ordering = ["order", "view_count", "create_time", "category","update_time", ]
    list_per_page = 20

    search_fields = ('title', 'cnt_md')

    filter_horizontal = ('label',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    }
    def save_model(self, request, obj, form, change):
        obj.user = request.user

        super().save_model(request, obj, form, change)
# 注册app的admin
admin.site.register(igaisdata, igaisdataadmin)
