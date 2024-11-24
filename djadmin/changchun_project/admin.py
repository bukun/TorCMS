from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ChangChunProject
from .resources import ChangChunProjectResource
from django.db import models
from django.forms import TextInput, Textarea
from leaflet.admin import LeafletGeoAdmin

# 设置默认的经纬度为长春市的大致中心点（纬度，经度）
DEFAULT_LOCATION = [43.88, 125.35]
class ChangChunProjectAdmin(LeafletGeoAdmin,ImportExportModelAdmin):
    resource_class = ChangChunProjectResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","cadastre_id", "name","xmdz","company","update_time")
    # 用来排序
    ordering = ["create_time","update_time",]
    list_per_page = 20
    default_zoom = 10  # 设置默认的缩放级别
    default_location = DEFAULT_LOCATION  # 设置默认显示的经纬度

    search_fields = ('name', 'cadastre_id')

    formfield_overrides = {
            models.CharField: {'widget': TextInput(attrs={'style': 'width: 80%;'})},
            models.TextField: {'widget': Textarea(attrs={'rows': 6, 'style': 'width: 80%;'})},
        }



# 注册app的admin
admin.site.register(ChangChunProject, ChangChunProjectAdmin)
