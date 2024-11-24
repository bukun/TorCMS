from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import farmpro
from .resources import FarmproResource
from django.db import models
from django.forms import TextInput, Textarea
class farmproadmin(ImportExportModelAdmin):
    resource_class = FarmproResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","product_name","address", "money", "unit", "date_update")
    # 用来排序
    # ordering = [ "date_update",]
    list_per_page = 20
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    }

    def save_model(self, request, obj, form, change):
        obj.user = request.user

        super().save_model(request, obj, form, change)

# 注册app的admin
admin.site.register(farmpro, farmproadmin)
