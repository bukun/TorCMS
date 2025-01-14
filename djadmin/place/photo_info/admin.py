from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from place.geofea.models  import Photoinfo
from .resources import PhotoinfoResource

class photoinfoadmin(ImportExportModelAdmin):
    resource_class = PhotoinfoResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ( "title", "lat",  "lon")
    ordering = ["id"]
    list_per_page = 20

    # 定义只读字段，这意味着它们在添加时不可编辑，但在更改时可编辑
    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj为None时表示添加，非None时表示编辑
            pass
        else:
            return ['lat', 'lon']
        return []


# 注册app的admin
admin.site.register(Photoinfo, photoinfoadmin)