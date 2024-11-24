from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import map
from .resources import MapResource

class mapadmin(ImportExportModelAdmin):
    resource_class = MapResource
    # 控制哪些字段会显示在Admin 的修改列表页面中
    list_display = (
        "id","title", "lat","lon","zoom_current","zoom_min","zoom_max")
    # 用来排序
    # ordering = ["order", "view_count", "create_time", "category", ]
    list_per_page = 20
    filter_horizontal = ('sites',)
    search_fields = ('title', 'id')

    # filter_horizontal = ('label',)
    # def get_category(self, obj):
    #     rec = Category.objects.get(id__exact=obj.category)
    #     return rec.name
    #
    # get_category.short_description = '分类名称'
    # get_category.admin_order_field = 'get_category'

# 注册app的admin
admin.site.register(map, mapadmin)
