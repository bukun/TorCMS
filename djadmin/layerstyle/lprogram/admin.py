from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import lprogram
# from .resources import lprogramResource
from django.db import models
from django.forms import TextInput, Textarea
class lprogramAdmin(ImportExportModelAdmin):
    # resource_class = lprogramResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","user","title","create_time","update_time")
    # 用来排序
    ordering = ["title","id","user"]
    list_per_page = 20
    filter_horizontal = ('sites',)
    search_fields = ("id",'title','user')

    # formfield_overrides = {
    #         models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
    #         models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    #         models.JSONField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    #     }


# 注册app的admin
admin.site.register(lprogram, lprogramAdmin)
