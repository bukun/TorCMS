from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ZNDatasetLabel
from .resources import LabelResource
from django.db.models.aggregates import Count


class ZNDatasetLabelAdmin(ImportExportModelAdmin):
    resource_class = LabelResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","name", "order", "get_count")
    # 用来排序
    ordering = ["order", ]
    list_per_page = 20

    def get_count(self, obj):
        rec = ZNDatasetLabel.objects.annotate(num_posts=Count('zn_dataset')).filter(name=obj.name)

        return rec[0].num_posts

    get_count.short_description = '数据数量'
    get_count.admin_order_field = 'get_count'


# 注册app的admin
admin.site.register(ZNDatasetLabel, ZNDatasetLabelAdmin)
