from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ThematicMaps
from .resources import ThematicMapsResource
from django.db import models
from django.forms import TextInput, Textarea
class ThematicMapsAdmin(ImportExportModelAdmin):
    resource_class = ThematicMapsResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("layer", "label","icon","create_time")
    # 用来排序
    ordering = ["layer","create_time",]
    list_per_page = 20

    search_fields = ('layer', 'label')

    formfield_overrides = {
            models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
            models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
        }


# 注册app的admin
admin.site.register(ThematicMaps, ThematicMapsAdmin)
