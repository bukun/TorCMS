from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import JupyterCatagory
from .resources import JupyterCatagoryResource
from mptt.admin import MPTTModelAdmin
from django.db.models.aggregates import Count


class JupyterCatagoryAdmin(ImportExportModelAdmin):
    resource_class = JupyterCatagoryResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = ("name", "order", "get_count",)


    list_per_page = 20
    filter_horizontal = ('sites',)
    def get_count(self, obj):
        rec = JupyterCatagory.objects.annotate(num_posts=Count('jupyter_data')).filter(name=obj.name)

        return rec[0].num_posts

    get_count.short_description = '数据数量'
    get_count.admin_order_field = 'get_count'


# 注册app的admin
admin.site.register(JupyterCatagory, JupyterCatagoryAdmin)