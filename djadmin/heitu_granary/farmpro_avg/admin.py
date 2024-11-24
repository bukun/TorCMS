from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import farmproavg
from .resources import FarmproAvgResource

class farmproavgadmin(ImportExportModelAdmin):
    resource_class = FarmproAvgResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","product_name", "avg", "address","unit","sample")
    # 用来排序
    ordering = ["avg"]
    list_per_page = 20
    def save_model(self, request, obj, form, change):
        obj.user = request.user

        super().save_model(request, obj, form, change)
# 注册app的admin
admin.site.register(farmproavg, farmproavgadmin)
