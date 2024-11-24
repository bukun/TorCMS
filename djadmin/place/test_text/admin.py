from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import TestText
from .resources import TestTextResource
from django.db import models
from django.forms import TextInput, Textarea
class TestTextAdmin(ImportExportModelAdmin):
    resource_class = TestTextResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","icon", "update_content")
    # 用来排序
    ordering = ["id"]
    list_per_page = 20

    search_fields = ("id",'txt')

    formfield_overrides = {
            models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
            models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
        }


# 注册app的admin
admin.site.register(TestText, TestTextAdmin)
