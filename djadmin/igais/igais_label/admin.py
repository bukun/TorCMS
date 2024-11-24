from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import igaislabel
from .resources import IgaisLabelResource
from django.db.models.aggregates import Count

class igaislabelsadmin(ImportExportModelAdmin):
    resource_class = IgaisLabelResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id", "name", "order", "get_count")
    # 用来排序
    ordering = ["name","order"]
    list_per_page = 20
    def get_count(self, obj):
        rec = igaislabel.objects.annotate(num_posts=Count('igaisdata')).filter(name=obj.name)

        return rec[0].num_posts

    get_count.short_description = '数据数量'
    get_count.admin_order_field = 'get_count'

# 注册app的admin
admin.site.register(igaislabel, igaislabelsadmin)
