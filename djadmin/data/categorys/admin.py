from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import categorys
from .resources import CategoryResource
from mptt.admin import MPTTModelAdmin
from django.db.models.aggregates import Count


class categoryadmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("id","name", "order", "get_count",)
    filter_horizontal = ('sites',)

    list_per_page = 20

    def get_count(self, obj):
        rec = categorys.objects.annotate(num_posts=Count('dataset')).filter(name=obj.name)

        return rec[0].num_posts

    get_count.short_description = '数据数量'
    get_count.admin_order_field = 'get_count'


# 注册app的admin
admin.site.register(categorys, categoryadmin)
