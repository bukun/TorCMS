from django.contrib import admin
from django.db.models.aggregates import Count
from import_export.admin import ImportExportModelAdmin
from mptt.admin import MPTTModelAdmin

from qgis.qgis_map.models import zhongbamapcategory

from .resources import ZhongbaMapCategoryResource


class zhongbamapcategoryadmin(ImportExportModelAdmin):
    resource_class = ZhongbaMapCategoryResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = (
        "name",
        "parent",
        "get_count",
    )

    list_per_page = 20
    filter_horizontal = ('sites',)

    def get_count(self, obj):
        rec = zhongbamapcategory.objects.annotate(
            num_posts=Count('zhongbadata')
        ).filter(name=obj.name)

        return rec[0].num_posts

    get_count.short_description = '数据数量'
    get_count.admin_order_field = 'count'


# 注册app的admin
admin.site.register(zhongbamapcategory, zhongbamapcategoryadmin)
