from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from place.geofea.models  import Geofea
from .resources import ApiAppResource
from django.db import models
from django.forms import TextInput, Textarea
class GeofeaAdmin(ImportExportModelAdmin):
    resource_class = ApiAppResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("title", "cnt_md","status","create_time")
    # 用来排序
    ordering = ["status","create_time",]
    list_per_page = 20

    search_fields = ('title', 'cnt_md')

    formfield_overrides = {
            models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
            models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
        }


# 注册app的admin
admin.site.register(Geofea, GeofeaAdmin)
