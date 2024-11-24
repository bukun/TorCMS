from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import igaiscategory
from .resources import IgaisCategoryResource

from django.db.models.aggregates import Count
from mptt.admin import MPTTModelAdmin

class igaiscategoryadmin(MPTTModelAdmin,ImportExportModelAdmin):
    resource_class = IgaisCategoryResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ( "name", "parent",  "get_count")
    ordering = ["name"]
    list_per_page = 20

    def get_count(self, obj):
        rec = igaiscategory.objects.annotate(num_posts=Count('igaisdata')).filter(name=obj.name)

        return rec[0].num_posts

    get_count.short_description = '数据数量'
    get_count.admin_order_field = 'count'


# 注册app的admin
admin.site.register(igaiscategory, igaiscategoryadmin)
