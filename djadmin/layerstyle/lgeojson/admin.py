from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import lgeojson
# from .resources import lgeojsonResource
from django.db import models
from django.forms import TextInput, Textarea
class lgeojsonAdmin(ImportExportModelAdmin):
    # resource_class = lgeojsonResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","title","create_time","update_time")
    # 用来排序
    ordering = ["title","id"]
    list_per_page = 20
    filter_horizontal = ('sites',)
    search_fields = ("id",'title')

    # formfield_overrides = {
    #         models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
    #         models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    #         models.JSONField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
    #     }


# 注册app的admin
admin.site.register(lgeojson, lgeojsonAdmin)
