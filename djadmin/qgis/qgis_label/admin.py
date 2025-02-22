from django.contrib import admin
from django.db.models.aggregates import Count
from import_export.admin import ImportExportModelAdmin

from qgis.qgis_map.models import QgisLabel

from .resources import LabelResource


class QgisLabelAdmin(ImportExportModelAdmin):
    resource_class = LabelResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = (
        "name",
        "get_count",
    )
    # 用来排序
    ordering = [
        "order",
    ]
    list_per_page = 20
    filter_horizontal = ('sites',)

    def get_count(self, obj):
        rec = QgisLabel.objects.annotate(num_posts=Count('qgismap')).filter(
            name=obj.name
        )

        return rec[0].num_posts

    get_count.short_description = '数据数量'
    get_count.admin_order_field = 'count'


# 注册app的admin
admin.site.register(QgisLabel, QgisLabelAdmin)
