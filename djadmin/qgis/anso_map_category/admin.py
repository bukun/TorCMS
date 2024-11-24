from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ANSOMapCategory
from .resources import ANSOMapCategoryResource

from django.db.models.aggregates import Count
from mptt.admin import MPTTModelAdmin

class ANSOCategoryadmin(ImportExportModelAdmin):
    resource_class = ANSOMapCategoryResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("name", "parent","get_count",)
    ordering = ['create_time']
    list_per_page = 20
    filter_horizontal = ('sites',)
    def get_count(self, obj):
        rec = ANSOMapCategory.objects.annotate(num_posts=Count('ansodata')).filter(name=obj.name)

        return rec[0].num_posts

    get_count.short_description = '数据数量'
    get_count.admin_order_field = 'count'


# 注册app的admin
admin.site.register(ANSOMapCategory, ANSOCategoryadmin)
